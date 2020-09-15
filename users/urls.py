"""Определяет схемы URL для пользователей"""
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name="login"),
    url(r'^logout/$', views.logout_view, name='logout'),
    # Страница регистрации
    url(r'^register/$', views.register, name='register'),
]

app_name = "users"
