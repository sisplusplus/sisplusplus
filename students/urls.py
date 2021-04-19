from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="students/login.html"),
        name="login",
    ),
]
