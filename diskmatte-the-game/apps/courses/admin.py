from django.contrib import admin

from .models import Chapter, Course, LearningSet


class LearningSetInline(admin.TabularInline):
	model = LearningSet
	extra = 0
	prepopulated_fields = {"slug": ("name",)}


class ChapterInline(admin.TabularInline):
	model = Chapter
	extra = 0
	prepopulated_fields = {"slug": ("title",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	inlines = [LearningSetInline]
	list_display = ("name", "slug", "is_active", "created_at")
	list_filter = ("is_active",)
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "description")


@admin.register(LearningSet)
class LearningSetAdmin(admin.ModelAdmin):
	inlines = [ChapterInline]
	list_display = ("name", "course", "kind", "order", "is_active")
	list_filter = ("kind", "is_active", "course")
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "description", "course__name")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
	list_display = ("title", "learning_set", "order", "is_active")
	list_filter = ("is_active", "learning_set__course")
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ("title", "description", "learning_set__name")
