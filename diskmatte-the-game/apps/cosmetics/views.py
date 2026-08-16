from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.progress.models import UserWallet

from .models import Skin, UserAvatar, UserSkin
from .services import equip_skin, purchase_skin


@login_required
def avatar(request):
    avatar_state, _ = UserAvatar.objects.get_or_create(user=request.user)
    owned_skins = UserSkin.objects.filter(user=request.user).select_related("skin")
    return render(
        request,
        "cosmetics/avatar.html",
        {"avatar": avatar_state, "owned_skins": owned_skins},
    )


@login_required
def shop(request):
    wallet, _ = UserWallet.objects.get_or_create(user=request.user)
    owned_skin_ids = set(
        UserSkin.objects.filter(user=request.user).values_list("skin_id", flat=True)
    )
    skins = Skin.objects.filter(is_available=True)
    return render(
        request,
        "cosmetics/shop.html",
        {"skins": skins, "owned_skin_ids": owned_skin_ids, "wallet": wallet},
    )


@login_required
def buy_skin(request, slug):
    if request.method != "POST":
        return redirect("cosmetics:shop")

    skin = get_object_or_404(Skin, slug=slug, is_available=True)
    try:
        result = purchase_skin(request.user, skin)
    except ValueError as error:
        messages.error(request, str(error))
    else:
        if result.purchased:
            messages.success(request, f"Du köpte {skin.name}! Du har {result.balance} disks kvar.")
        else:
            messages.info(request, "Du äger redan detta skin.")
    return redirect("cosmetics:shop")


@login_required
def equip_skin_view(request, slug):
    if request.method != "POST":
        return redirect("cosmetics:avatar")

    skin = get_object_or_404(Skin, slug=slug)
    try:
        equip_skin(request.user, skin)
    except ValueError as error:
        messages.error(request, str(error))
    else:
        messages.success(request, f"{skin.name} är nu utrustat.")
    return redirect("cosmetics:avatar")
