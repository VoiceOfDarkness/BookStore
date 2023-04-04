from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationFrom


CustomUser = get_user_model()
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFrom
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username')
