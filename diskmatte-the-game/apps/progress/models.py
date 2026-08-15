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
