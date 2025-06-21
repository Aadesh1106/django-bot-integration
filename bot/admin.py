from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'first_name', 'django_user', 'created_at', 'is_active']
    list_filter = ['created_at', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    list_editable = ['is_active']