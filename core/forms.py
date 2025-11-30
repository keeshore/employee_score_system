from django import forms
from django.contrib.auth.models import User
from .models import Employee

class RegisterForm(forms.Form):
    emp_id = forms.CharField(max_length=20)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    company = forms.CharField(max_length=100)

    POSITION_CHOICES = [
        ("HR", "HR"),
        ("Manager", "Manager"),
        ("Team Leader", "Team Leader"),
        ("Employee", "Employee"),
    ]
    position = forms.ChoiceField(choices=POSITION_CHOICES)
