from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('subscribed_products',)}),  # 추가 필드
    )

admin.site.register(CustomUser, CustomUserAdmin)
