from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'role')

admin.site.register(CustomUser, CustomUserAdmin)