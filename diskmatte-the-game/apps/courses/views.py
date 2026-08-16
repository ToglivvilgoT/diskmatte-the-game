from django.shortcuts import get_object_or_404, render

from apps.progress.models import TaskCompletion
from apps.tasks.models import Task

from .models import Course, LearningSet, Topic


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    learning_sets = course.learning_sets.filter(is_active=True)
    for learning_set in learning_sets:
        learning_set.total_tasks = learning_set.tasks.filter(is_published=True).count()
        learning_set.solved_tasks = 0
        if request.user.is_authenticated:
            learning_set.solved_tasks = TaskCompletion.objects.filter(
                user=request.user,
                task__learning_set=learning_set,
                task__is_published=True,
            ).count()
        learning_set.completion_percentage = (
            round(learning_set.solved_tasks / learning_set.total_tasks * 100)
            if learning_set.total_tasks
            else 0
        )
    course.total_tasks = sum(learning_set.total_tasks for learning_set in learning_sets)
    course.solved_tasks = sum(learning_set.solved_tasks for learning_set in learning_sets)
    course.completion_percentage = (
        round(course.solved_tasks / course.total_tasks * 100)
        if course.total_tasks
        else 0
    )
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
    total_tasks = tasks.count()
    completed_task_ids = set()
    if request.user.is_authenticated:
        completed_task_ids = set(
            TaskCompletion.objects.filter(
                user=request.user,
                task__learning_set=learning_set,
            ).values_list("task_id", flat=True)
        )
    solved_tasks = len(completed_task_ids)
    for task in tasks:
        task.is_completed = task.pk in completed_task_ids

    return render(
        request,
        "courses/learning_set_detail.html",
        {
            "course": course,
            "learning_set": learning_set,
            "tasks": tasks,
            "total_tasks": total_tasks,
            "solved_tasks": solved_tasks,
            "completion_percentage": round(solved_tasks / total_tasks * 100) if total_tasks else 0,
        },
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
