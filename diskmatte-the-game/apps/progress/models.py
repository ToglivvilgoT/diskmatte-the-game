from django.conf import settings
from django.db import models

from apps.tasks.models import Task


class TaskCompletion(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	completed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-completed_at"]
		constraints = [
			models.UniqueConstraint(
				fields=("user", "task"),
				name="unique_user_task_completion",
			)
		]

	def __str__(self):
		return f"{self.user} completed {self.task}"


class UserWallet(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	balance = models.PositiveIntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user} wallet ({self.balance} disks)"


class DiskTransaction(models.Model):
	class TransactionType(models.TextChoices):
		TASK_REWARD = "task_reward", "Task reward"
		SKIN_PURCHASE = "skin_purchase", "Skin purchase"
		ADMIN_ADJUSTMENT = "admin_adjustment", "Admin adjustment"

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	transaction_type = models.CharField(max_length=30, choices=TransactionType.choices)
	task_completion = models.OneToOneField(
		TaskCompletion,
		null=True,
		blank=True,
		on_delete=models.PROTECT,
	)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.user}: {self.amount} disks"
