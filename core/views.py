from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Employee, ScoreHistory
from .forms import RegisterForm

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings


# -------------------------------------------------
# BASIC PAGES
# -------------------------------------------------

def home(request):
    return render(request, "core/home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            emp_id = form.cleaned_data["emp_id"]
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            company = form.cleaned_data["company"]
            position = form.cleaned_data["position"]

            user = User.objects.create_user(
                username=emp_id,
                first_name=full_name,
                email=email,
                password=password
            )

            Employee.objects.create(
                user=user,
                emp_id=emp_id,
                company=company,
                position=position,
                score=0
            )

            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        password = request.POST.get("password")

        user = authenticate(username=emp_id, password=password)

        if user:
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "core/login.html", {
                "error": "Invalid Employee ID or Password"
            })

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------------------------------
# PROFILE PAGE
# -------------------------------------------------

@login_required
def profile(request):
    employee = Employee.objects.get(user=request.user)
    history = ScoreHistory.objects.filter(employee=employee).order_by('-timestamp')

    return render(request, "core/profile.html", {
        "employee": employee,
        "history": history
    })


# -------------------------------------------------
# ADD SCORE PAGE (UI only)
# -------------------------------------------------

@login_required
def add_score(request):
    current_user = Employee.objects.get(user=request.user)

    allowed_positions = ["HR", "Manager", "Team Leader"]
    if current_user.position not in allowed_positions:
        return render(request, "core/not_allowed.html")

    target = None

    if request.method == "POST":

        # SEARCH employee
        if "search" in request.POST:
            company = request.POST.get("company_name")
            emp_id = request.POST.get("emp_id")

            try:
                target = Employee.objects.get(emp_id=emp_id, company=company)
            except Employee.DoesNotExist:
                messages.error(request, "Employee not found in this company.")
                return redirect("add_score")

        # ADD SCORE
        elif "addscore" in request.POST:
            emp_id = request.POST.get("emp_id")
            score_added = int(request.POST.get("score_added"))
            description = request.POST.get("description")

            try:
                target = Employee.objects.get(emp_id=emp_id)
            except Employee.DoesNotExist:
                messages.error(request, "Employee not found.")
                return redirect("add_score")

            if score_added > 2:
                messages.error(request, "Only +2 score allowed.")
                return redirect("add_score")

            # hierarchy check
            hierarchy = ["Employee", "Team Leader", "Manager", "HR"]
            if hierarchy.index(current_user.position) <= hierarchy.index(target.position):
                return render(request, "core/not_allowed.html")

            # update score
            target.score += score_added
            target.save()

            # add history
            ScoreHistory.objects.create(
                employee=target,
                added_by=current_user,
                score_added=score_added,
                description=description,
                timestamp=timezone.now()
            )

            messages.success(request, "Score added successfully!")
            return redirect("profile")

    return render(request, "core/add_score.html", {"target": target})


# -------------------------------------------------
# API FUNCTIONS
# -------------------------------------------------

def _check_api_key(request):
    key = request.headers.get("X-API-KEY") or request.META.get("HTTP_X_API_KEY")
    return key == settings.API_KEY_FOR_ZOHO


def api_get_score(request, emp_id):
    try:
        emp = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Employee not found"}, status=404)

    return JsonResponse({
        "status": "success",
        "emp_id": emp.emp_id,
        "name": emp.user.first_name,
        "company": emp.company,
        "position": emp.position,
        "score": emp.score
    })


@csrf_exempt
def api_search_employee(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    if not _check_api_key(request):
        return HttpResponseForbidden("Invalid API key")

    try:
        data = json.loads(request.body.decode("utf-8"))
        company = data.get("company")
        emp_id = data.get("emp_id")
    except:
        return HttpResponseBadRequest("Invalid JSON")

    try:
        emp = Employee.objects.get(emp_id=emp_id, company=company)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Employee not found"}, status=404)

    return JsonResponse({
        "status": "success",
        "emp_id": emp.emp_id,
        "name": emp.user.first_name,
        "company": emp.company,
        "position": emp.position,
        "score": emp.score
    })


@csrf_exempt
def api_add_score(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    if not _check_api_key(request):
        return HttpResponseForbidden("Invalid API key")

    try:
        data = json.loads(request.body.decode("utf-8"))
        target_emp_id = data.get("emp_id")
        actor_emp_id = data.get("actor_emp_id")
        score_added = int(data.get("score_added"))
        description = data.get("description")
    except:
        return HttpResponseBadRequest("Invalid JSON")

    try:
        target = Employee.objects.get(emp_id=target_emp_id)
        actor = Employee.objects.get(emp_id=actor_emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Employee not found"}, status=404)

    if score_added > 2:
        return JsonResponse({"status": "error", "message": "Maximum +2 allowed"}, status=400)

    hierarchy = ["Employee", "Team Leader", "Manager", "HR"]
    if hierarchy.index(actor.position) <= hierarchy.index(target.position):
        return JsonResponse({"status": "error", "message": "Permission denied (hierarchy)"}, status=403)

    target.score += score_added
    target.save()

    ScoreHistory.objects.create(
        employee=target,
        added_by=actor,
        score_added=score_added,
        description=description,
        timestamp=timezone.now()
    )

    return JsonResponse({
        "status": "success",
        "message": "Score added successfully",
        "emp_id": target.emp_id,
        "new_score": target.score
    })
