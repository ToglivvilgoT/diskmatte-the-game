from django.shortcuts import get_object_or_404, render

from .models import Course, LearningSet, Topic


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    learning_sets = course.learning_sets.filter(is_active=True)
    learning_set_topics = [
        (
            learning_set,
            Topic.objects.filter(
                course=course,
                tasks__learning_set=learning_set,
            ).distinct(),
        )
        for learning_set in learning_sets
    ]
    return render(
        request,
        "courses/course_detail.html",
        {"course": course, "learning_set_topics": learning_set_topics},
    )


def topic_detail(request, course_slug, learning_set_slug, slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=learning_set_slug,
        is_active=True,
    )
    topic = get_object_or_404(Topic, course=course, slug=slug, is_active=True)
    tasks = topic.tasks.filter(learning_set=learning_set, is_published=True)
    return render(
        request,
        "courses/topic_detail.html",
        {"course": course, "learning_set": learning_set, "topic": topic, "tasks": tasks},
    )
