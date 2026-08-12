from django.shortcuts import get_object_or_404, render

from .models import Chapter, Course, LearningSet


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


def chapter_detail(request, course_slug, learning_set_slug, slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    learning_set = get_object_or_404(
        LearningSet,
        course=course,
        slug=learning_set_slug,
        is_active=True,
    )
    chapter = get_object_or_404(Chapter, learning_set=learning_set, slug=slug, is_active=True)
    tasks = chapter.tasks.filter(is_published=True)
    return render(
        request,
        "courses/chapter_detail.html",
        {"course": course, "learning_set": learning_set, "chapter": chapter, "tasks": tasks},
    )
