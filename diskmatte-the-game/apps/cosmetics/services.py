from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction

from apps.progress.models import DiskTransaction, UserWallet

from .models import Skin, UserAvatar, UserSkin


@dataclass(frozen=True)
class PurchaseResult:
    purchased: bool
    balance: int


def purchase_skin(user, skin: Skin) -> PurchaseResult:
    """Buy a skin once while keeping the wallet and ledger consistent."""
    user_model = get_user_model()
    with db_transaction.atomic():
        locked_user = user_model.objects.select_for_update().get(pk=user.pk)
        wallet, _ = UserWallet.objects.get_or_create(user=locked_user)
        wallet = UserWallet.objects.select_for_update().get(pk=wallet.pk)

        if UserSkin.objects.filter(user=locked_user, skin=skin).exists():
            return PurchaseResult(False, wallet.balance)
        if wallet.balance < skin.price:
            raise ValueError("Otillräckligt antal disks.")

        wallet.balance -= skin.price
        wallet.save(update_fields=["balance", "updated_at"])
        UserSkin.objects.create(user=locked_user, skin=skin)
        DiskTransaction.objects.create(
            user=locked_user,
            amount=-skin.price,
            transaction_type=DiskTransaction.TransactionType.SKIN_PURCHASE,
            description=f"Köp av skin: {skin.name}",
        )

        return PurchaseResult(True, wallet.balance)


def equip_skin(user, skin: Skin) -> None:
    """Equip a skin only if the user owns it."""
    if not UserSkin.objects.filter(user=user, skin=skin).exists():
        raise ValueError("Du äger inte detta skin.")

    UserAvatar.objects.update_or_create(
        user=user,
        defaults={"equipped_skin": skin},
    )
