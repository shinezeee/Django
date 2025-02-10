from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "name", "is_active", "is_staff")  # 표시할 필드
    list_filter = ("is_active", "is_staff")  # 필터 옵션
    search_fields = ("email", "name")  # 검색 가능 필드
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    ordering = ["email"]