from django.shortcuts import get_object_or_404, render

from apps.courses.models import Chapter, Course, LearningSet

from .models import Task


def task_detail(request, course_slug, learning_set_slug, chapter_slug, slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=learning_set_slug,
        is_active=True,
    )
    chapter = get_object_or_404(Chapter, learning_set=learning_set, slug=chapter_slug, is_active=True)
    task = get_object_or_404(Task, learning_set=learning_set, chapter=chapter, slug=slug, is_published=True)
    return render(
        request,
        "tasks/task_detail.html",
        {"course": course, "learning_set": learning_set, "chapter": chapter, "task": task},
    )
