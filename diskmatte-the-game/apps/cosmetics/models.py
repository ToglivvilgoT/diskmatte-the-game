from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Skin(models.Model):
    class Kind(models.TextChoices):
        COLOR = "color", "Färg"
        IMAGE = "image", "Bild"
        CSS_CLASS = "css_class", "CSS-klass"

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.COLOR)
    color = models.CharField(max_length=7, default="#de2a2a")
    image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Sökväg relativt static/, t.ex. cosmetics/skins/lava.png",
    )
    css_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="CSS-klass definierad i skins.css, t.ex. skin-galax",
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price", "name"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.kind == self.Kind.IMAGE and not self.image:
            raise ValidationError({"image": "Bild krävs för skin av typen Bild."})
        if self.kind == self.Kind.CSS_CLASS and not self.css_class:
            raise ValidationError({"css_class": "CSS-klass krävs för skin av typen CSS-klass."})


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
