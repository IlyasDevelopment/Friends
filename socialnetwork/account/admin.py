from django.contrib import admin
from .models import User, FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
