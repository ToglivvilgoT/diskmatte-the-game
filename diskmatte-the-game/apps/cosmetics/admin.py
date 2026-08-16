from django.contrib import admin

from .models import Skin, UserAvatar, UserSkin


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "price", "is_available", "created_at")
    list_filter = ("kind", "is_available")
    prepopulated_fields = {"slug": ("name",)}
    fields = (
        "name",
        "slug",
        "description",
        "price",
        "kind",
        "color",
        "image",
        "is_available",
    )


@admin.register(UserSkin)
class UserSkinAdmin(admin.ModelAdmin):
    list_display = ("user", "skin", "purchased_at")
    search_fields = ("user__username", "skin__name")


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ("user", "equipped_skin")
    search_fields = ("user__username",)
