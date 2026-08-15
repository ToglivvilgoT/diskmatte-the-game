from django.shortcuts import get_object_or_404, render

from .models import Course, LearningSet, Topic


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    learning_sets = course.learning_sets.filter(is_active=True)
    return render(
        request,
        "courses/course_detail.html",
        {"course": course, "learning_sets": learning_sets},
    )


def learning_set_detail(request, course_slug, slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=slug,
        is_active=True,
    )
    tasks = learning_set.tasks.filter(is_published=True).select_related("topic")
    return render(
        request,
        "courses/learning_set_detail.html",
        {"course": course, "learning_set": learning_set, "tasks": tasks},
    )


def topic_detail(request, course_slug, learning_set_slug, topic_slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=learning_set_slug,
        is_active=True,
    )
    topic = get_object_or_404(Topic, course=course, slug=topic_slug, is_active=True)
    tasks = topic.tasks.filter(learning_set=learning_set, is_published=True)
    return render(
        request,
        "courses/topic_detail.html",
        {"course": course, "learning_set": learning_set, "topic": topic, "tasks": tasks},
    )
