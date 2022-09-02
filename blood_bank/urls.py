from django.urls import path
from blood_bank import views

app_name = 'blood_bank'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
