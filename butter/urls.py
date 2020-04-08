from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.project_list, name='list'),
    path('register', user_views.register, name = 'register'),
    path('login', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    path('profile', user_views.profile, name = 'profile'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.project_detail, name='detail')
]
