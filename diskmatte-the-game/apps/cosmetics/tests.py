import tempfile
from io import StringIO
from pathlib import Path

from django.contrib.auth import get_user_model
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


class SyncSkinImagesCommandTests(TestCase):
    def test_creates_unavailable_skin_for_new_image_and_skips_existing(self):
        Skin.objects.create(
            name="Solhjälten",
            slug="lava",
            price=100,
            color="#f0a202",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            skins_dir = Path(tmp_dir) / "static" / "cosmetics" / "skins"
            skins_dir.mkdir(parents=True)
            (skins_dir / "lava.png").write_bytes(b"")
            (skins_dir / "ice_king.png").write_bytes(b"")
            (skins_dir / "notes.txt").write_bytes(b"")

            with override_settings(BASE_DIR=Path(tmp_dir)):
                out = StringIO()
                call_command("sync_skin_images", stdout=out)

        self.assertFalse(
            Skin.objects.get(slug="ice-king").is_available,
        )
        self.assertEqual(
            Skin.objects.get(slug="ice-king").image,
            "cosmetics/skins/ice_king.png",
        )
        self.assertEqual(Skin.objects.filter(slug="lava").count(), 1)
        self.assertIn("Created skin: ice-king", out.getvalue())
        self.assertIn("Already exists, skipped: lava", out.getvalue())

