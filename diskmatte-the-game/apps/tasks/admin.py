from django.contrib import admin

from .models import Task, TaskOption


class TaskOptionInline(admin.TabularInline):
	model = TaskOption
	extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	inlines = [TaskOptionInline]
	list_display = ("title", "learning_set", "topic", "answer_type", "order", "is_published")
	list_filter = ("answer_type", "is_published", "learning_set")
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ("title", "prompt", "book_reference")


@admin.register(TaskOption)
class TaskOptionAdmin(admin.ModelAdmin):
	list_display = ("label", "task", "position", "is_correct")
	list_filter = ("is_correct",)
	search_fields = ("label", "task__title")
