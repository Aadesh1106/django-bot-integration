from django.contrib import admin
from .models import UserProfile, Post

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_username', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'telegram_username']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']