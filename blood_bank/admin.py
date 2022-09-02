from django.contrib import admin
from blood_bank.models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

admin.autodiscover()
admin.site.enable_nav_sidebar = False

class MyUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser

   
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    model = MyUser
    ordering = ['username']
    list_display   = ['username','email','birth_date','user_type']

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ['user_type']}),
    )

admin.site.register(MyUser, MyUserAdmin)
