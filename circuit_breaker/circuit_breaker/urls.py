from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('success/', views.success_endpoint),
    path('failure/', views.faulty_endpoint),
]
