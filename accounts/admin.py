from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Modify the existing fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address','role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_of_birth', 'date_joined')}),
    )
    
    # Add the fields to the add form as well
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone', 'address', 'role'),
        }),
    )
    
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'phone', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'role', 'phone')

admin.site.register(CustomUser, CustomUserAdmin)