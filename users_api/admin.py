from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )
    list_filter = UserAdmin.list_filter + ('role',)
    search_fields = UserAdmin.search_fields + ('role',)
