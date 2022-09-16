from django.urls import path
from blood_bank import views

app_name = 'blood_bank'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    
    path('create-donor-perfil/', views.CreatePerfil.as_view(), 'create_donor_perfil' ),
    path('edit-donor-perfil/<int:pk>', views.CreatePerfil.as_view(), 'edit_donor_perfil' ),
    
]
