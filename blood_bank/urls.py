from django.urls import path
from blood_bank.views import Signup

app_name = 'blood_bank'

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
]
