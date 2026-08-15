from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction

from apps.tasks.models import Task

from .models import DiskTransaction, TaskCompletion, UserWallet


@dataclass(frozen=True)
class TaskRewardResult:
    awarded: bool
    disks_earned: int
    balance: int


def complete_task(user, task: Task) -> TaskRewardResult:
    """Complete a task once and award its configured disk reward once."""
    user_model = get_user_model()
    with db_transaction.atomic():
        locked_user = user_model.objects.select_for_update().get(pk=user.pk)
        completion, created = TaskCompletion.objects.get_or_create(
            user=locked_user,
            task=task,
        )
        wallet, _ = UserWallet.objects.get_or_create(user=locked_user)
        wallet = UserWallet.objects.select_for_update().get(pk=wallet.pk)

        if not created:
            return TaskRewardResult(False, 0, wallet.balance)

        wallet.balance += task.disk_reward
        wallet.save(update_fields=["balance", "updated_at"])
        DiskTransaction.objects.create(
            user=locked_user,
            amount=task.disk_reward,
            transaction_type=DiskTransaction.TransactionType.TASK_REWARD,
            task_completion=completion,
            description=f"Belöning för uppgiften: {task.title}",
        )

        return TaskRewardResult(True, task.disk_reward, wallet.balance)