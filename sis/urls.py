from django.urls import path
from sis import views

urlpatterns = [
    path('faculties/', views.faculty_list),
    path('faculties/<str:pk>/', views.faculty_detail),
    ]
