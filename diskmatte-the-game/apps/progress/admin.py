from django.contrib import admin

from .models import DiskTransaction, TaskCompletion, UserWallet


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
	list_display = ("user", "task", "completed_at")
	list_filter = ("completed_at",)
	search_fields = ("user__username", "task__title")


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
	list_display = ("user", "balance", "updated_at")
	search_fields = ("user__username",)


@admin.register(DiskTransaction)
class DiskTransactionAdmin(admin.ModelAdmin):
	list_display = ("user", "amount", "transaction_type", "task_completion", "created_at")
	list_filter = ("transaction_type", "created_at")
	search_fields = ("user__username", "description")
