from django.shortcuts import get_object_or_404, render

from apps.courses.models import Course, LearningSet, Topic

from .models import Task


def task_detail(request, course_slug, learning_set_slug, topic_slug, slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=learning_set_slug,
        is_active=True,
    )
    topic = get_object_or_404(Topic, course=course, slug=topic_slug, is_active=True)
    task = get_object_or_404(Task, learning_set=learning_set, topic=topic, slug=slug, is_published=True)
    return render(
        request,
        "tasks/task_detail.html",
        {"course": course, "learning_set": learning_set, "topic": topic, "task": task},
    )
