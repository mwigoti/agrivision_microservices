from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ('email', 'username', 'is_staff', 'is_email_verified', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_email_verified')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)

    # Define the fieldsets for adding and changing user information
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('is_email_verified', 'verification_token')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields for the add user form in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register the CustomUser model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)
