from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add-score/', views.add_score, name='add_score'),
    path('profile/', views.profile, name='profile'),
    path('add-score/', views.add_score, name='add_score'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-score/', views.add_score, name='add_score'),
    path('api/get-score/<str:emp_id>/', views.api_get_score, name='api_get_score'),
    path('api/search-employee/', views.api_search_employee, name='api_search_employee'),
    path('api/add-score/', views.api_add_score, name='api_add_score'),
]
