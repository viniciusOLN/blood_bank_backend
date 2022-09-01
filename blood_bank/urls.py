from django.urls import path
from blood_bank import views
from rest_framework import routers
from django.conf.urls import include

app_name = 'blood_bank'

urlpatterns = [
    path('login/', views.login, name='login'),
]
