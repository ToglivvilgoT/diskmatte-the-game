from django.contrib import admin

from .models import Skin, UserAvatar, UserSkin


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available", "created_at")
    list_filter = ("is_available",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(UserSkin)
class UserSkinAdmin(admin.ModelAdmin):
    list_display = ("user", "skin", "purchased_at")
    search_fields = ("user__username", "skin__name")


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ("user", "equipped_skin")
    search_fields = ("user__username",)
