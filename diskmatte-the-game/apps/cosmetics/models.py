from django.conf import settings
from django.db import models


class Skin(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    color = models.CharField(max_length=7, default="#2457a6")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price", "name"]

    def __str__(self):
        return self.name


class UserSkin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-purchased_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("user", "skin"),
                name="unique_user_skin",
            )
        ]

    def __str__(self):
        return f"{self.user} owns {self.skin}"


class UserAvatar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equipped_skin = models.ForeignKey(
        Skin,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.user} avatar"
