import tempfile
from io import StringIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.progress.models import DiskTransaction, UserWallet

from .models import Skin, UserAvatar, UserSkin


class CosmeticsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student",
            password="test-password",
        )
        self.skin = Skin.objects.create(
            name="Solhjälten",
            slug="solhjalten",
            description="Lite extra energi.",
            price=100,
            color="#f0a202",
        )

    def test_shop_requires_login(self):
        response = self.client.get(reverse("cosmetics:shop"))

        self.assertRedirects(response, "/accounts/login/?next=/avatar/shop/")

    def test_user_can_buy_skin_and_disks_are_logged(self):
        UserWallet.objects.create(user=self.user, balance=150)
        self.client.login(username="student", password="test-password")

        response = self.client.post(reverse("cosmetics:buy-skin", args=(self.skin.slug,)))

        self.assertRedirects(response, reverse("cosmetics:shop"))
        self.assertTrue(UserSkin.objects.filter(user=self.user, skin=self.skin).exists())
        self.assertEqual(UserWallet.objects.get(user=self.user).balance, 50)
        self.assertEqual(
            DiskTransaction.objects.get(user=self.user).amount,
            -100,
        )

    def test_user_cannot_buy_skin_without_enough_disks(self):
        UserWallet.objects.create(user=self.user, balance=99)
        self.client.login(username="student", password="test-password")

        self.client.post(reverse("cosmetics:buy-skin", args=(self.skin.slug,)))

        self.assertFalse(UserSkin.objects.filter(user=self.user, skin=self.skin).exists())
        self.assertEqual(UserWallet.objects.get(user=self.user).balance, 99)
        self.assertFalse(DiskTransaction.objects.filter(user=self.user).exists())

    def test_user_cannot_buy_same_skin_twice(self):
        UserWallet.objects.create(user=self.user, balance=250)
        self.client.login(username="student", password="test-password")
        buy_url = reverse("cosmetics:buy-skin", args=(self.skin.slug,))

        self.client.post(buy_url)
        self.client.post(buy_url)

        self.assertEqual(UserSkin.objects.filter(user=self.user, skin=self.skin).count(), 1)
        self.assertEqual(UserWallet.objects.get(user=self.user).balance, 150)
        self.assertEqual(DiskTransaction.objects.filter(user=self.user).count(), 1)

    def test_user_can_equip_owned_skin(self):
        UserSkin.objects.create(user=self.user, skin=self.skin)
        self.client.login(username="student", password="test-password")

        response = self.client.post(
            reverse("cosmetics:equip-skin", args=(self.skin.slug,)),
        )

        self.assertRedirects(response, reverse("cosmetics:avatar"))
        self.assertEqual(
            UserAvatar.objects.get(user=self.user).equipped_skin,
            self.skin,
        )


class SkinValidationTests(TestCase):
    def test_css_class_skin_requires_css_class(self):
        skin = Skin(
            name="Galax",
            slug="galax",
            price=100,
            kind=Skin.Kind.CSS_CLASS,
        )

        with self.assertRaises(ValidationError):
            skin.full_clean()

    def test_css_class_skin_is_valid_with_css_class(self):
        skin = Skin(
            name="Galax",
            slug="galax",
            price=100,
            kind=Skin.Kind.CSS_CLASS,
            css_class="skin-galaxy",
        )

        skin.full_clean()

    def test_image_skin_requires_image(self):
        skin = Skin(
            name="Lava",
            slug="lava",
            price=100,
            kind=Skin.Kind.IMAGE,
        )

        with self.assertRaises(ValidationError):
            skin.full_clean()


class SkinRenderingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student",
            password="test-password",
        )
        self.css_skin = Skin.objects.create(
            name="Galax",
            slug="galax",
            price=0,
            kind=Skin.Kind.CSS_CLASS,
            css_class="skin-galaxy",
        )

    def test_shop_renders_css_class_skin(self):
        self.client.login(username="student", password="test-password")

        response = self.client.get(reverse("cosmetics:shop"))

        self.assertContains(response, "skin-galaxy")

    def test_avatar_renders_equipped_css_class_skin(self):
        UserSkin.objects.create(user=self.user, skin=self.css_skin)
        UserAvatar.objects.create(user=self.user, equipped_skin=self.css_skin)
        self.client.login(username="student", password="test-password")

        response = self.client.get(reverse("cosmetics:avatar"))

        self.assertContains(response, "skin-galaxy")


class SyncSkinImagesCommandTests(TestCase):
    def test_marks_skins_missing_from_metadata_unavailable(self):
        missing_skin = Skin.objects.create(
            name="Solhjälten",
            slug="solhjalten",
            price=100,
            color="#f0a202",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            skins_dir = Path(tmp_dir) / "static" / "cosmetics" / "skins"
            skins_dir.mkdir(parents=True)
            (skins_dir / "metadata.json").write_text(
                '[{"name": "Lava", "slug": "lava", "description": "", '
                '"price": 100, "kind": "COLOR", "color": "#f0a202"}]',
                encoding="utf-8",
            )

            with override_settings(BASE_DIR=Path(tmp_dir)):
                out = StringIO()
                call_command("sync_skin_images", stdout=out)

        missing_skin.refresh_from_db()
        self.assertFalse(missing_skin.is_available)
        self.assertIn(
            "Skin 'solhjalten' missing from metadata, marking unavailable",
            out.getvalue(),
        )

    def test_creates_unavailable_skin_and_skips_existing(self):
        Skin.objects.create(
            name="Solhjälten",
            slug="lava",
            price=100,
            color="#f0a202",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            skins_dir = Path(tmp_dir) / "static" / "cosmetics" / "skins"
            skins_dir.mkdir(parents=True)
            (skins_dir / "metadata.json").write_text(
                '[{"name": "Solhjälten", "slug": "lava", "description": "", '
                '"price": 100, "kind": "COLOR", "color": "#f0a202"}, '
                '{"name": "Iskungen", "slug": "ice-king", "description": "", '
                '"price": 100, "kind": "IMAGE"}]',
                encoding="utf-8",
            )

            with override_settings(BASE_DIR=Path(tmp_dir)):
                out = StringIO()
                call_command("sync_skin_images", stdout=out)

        self.assertFalse(
            Skin.objects.get(slug="ice-king").is_available,
        )
        self.assertEqual(Skin.objects.filter(slug="lava").count(), 1)
        self.assertIn("Created skin 'ice-king'", out.getvalue())
        self.assertIn("Updated skin: lava", out.getvalue())

