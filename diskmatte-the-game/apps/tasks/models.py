from typing import TYPE_CHECKING

from django.db import models

from apps.courses.models import LearningSet, Topic


class Task(models.Model):
    if TYPE_CHECKING:
        # Reverse relation created by TaskOption.task with related_name="options".
        options: models.Manager["TaskOption"]

    class AnswerType(models.TextChoices):
        CHECKBOX = "checkbox", "Checkbox"
        INPUT_FIELD = "input_field", "Input field"
        MULTIPLE_CHOICE = "multiple_choice", "Multiple choice"

    learning_set = models.ForeignKey(LearningSet, related_name="tasks", on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name="tasks", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    prompt = models.TextField()
    instructions = models.TextField(blank=True)
    answer_type = models.CharField(
        max_length=24,
        choices=AnswerType.choices,
        default=AnswerType.INPUT_FIELD,
    )
    expected_answer = models.TextField(blank=True)
    hint = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    external_link = models.URLField(blank=True)
    book_reference = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        unique_together = ("learning_set", "slug")

    def __str__(self):
        return self.title


class TaskOption(models.Model):
    task = models.ForeignKey(Task, related_name="options", on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.label
