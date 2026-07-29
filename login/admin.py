from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email','username','ruolo','is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Infromazioni extra', {'fields': ('ruolo','telefono')}),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        ('Infromazioni extra', {'fields': ('ruolo','telefono')}),
    ) 

admin.site.register(CustomUser,CustomUserAdmin)