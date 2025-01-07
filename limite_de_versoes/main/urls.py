from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.form_screen, name='form_screen'),
    path('process_data/', views.process_data, name='process_data')
]
