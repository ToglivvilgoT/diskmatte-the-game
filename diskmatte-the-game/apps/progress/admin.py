from django.contrib import admin

from .models import TaskCompletion


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
	list_display = ("user", "task", "completed_at")
	list_filter = ("completed_at",)
	search_fields = ("user__username", "task__title")
