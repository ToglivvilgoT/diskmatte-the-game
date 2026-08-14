from django.contrib import admin

from .models import Course, LearningSet, Topic


class LearningSetInline(admin.TabularInline):
	model = LearningSet
	extra = 0
	prepopulated_fields = {"slug": ("name",)}


class TopicInline(admin.TabularInline):
	model = Topic
	extra = 0
	prepopulated_fields = {"slug": ("title",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	inlines = [LearningSetInline, TopicInline]
	list_display = ("name", "slug", "is_active", "created_at")
	list_filter = ("is_active",)
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "description")


@admin.register(LearningSet)
class LearningSetAdmin(admin.ModelAdmin):
	list_display = ("name", "course", "kind", "order", "is_active")
	list_filter = ("kind", "is_active", "course")
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ("name", "description", "course__name")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ("title", "course", "order", "is_active")
	list_filter = ("is_active", "course")
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ("title", "description", "course__name")
