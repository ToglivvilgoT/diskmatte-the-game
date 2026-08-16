from django.urls import path

from .views import avatar, buy_skin, equip_skin_view, shop

app_name = "cosmetics"

urlpatterns = [
    path("", avatar, name="avatar"),
    path("shop/", shop, name="shop"),
    path("shop/<slug:slug>/buy/", buy_skin, name="buy-skin"),
    path("skins/<slug:slug>/equip/", equip_skin_view, name="equip-skin"),
]
