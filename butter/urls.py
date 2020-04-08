from django.contrib import admin
from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.project_list, name='list'),
    path('register', user_views.register, name = 'register'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.project_detail, name='detail')
]
