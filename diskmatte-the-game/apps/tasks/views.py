from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from apps.courses.models import Course, LearningSet, Topic
from apps.progress.services import complete_task

from .models import Task


@login_required
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
    is_correct = None
    next_task = None
    reward_result = None
    if request.method == "POST":
        if task.answer_type == Task.AnswerType.CHECKBOX:
            is_correct = request.POST.get("answer") == "on"
        elif task.answer_type == Task.AnswerType.MULTIPLE_CHOICE:
            selected_option = task.options.filter(pk=request.POST.get("answer")).first()
            is_correct = selected_option is not None and selected_option.is_correct
        else:
            submitted_answer = request.POST.get("answer", "").strip()
            is_correct = submitted_answer.casefold() == task.expected_answer.strip().casefold()

        if is_correct:
            reward_result = complete_task(request.user, task)
            task_list = list(
                Task.objects.filter(learning_set=learning_set, is_published=True)
                .select_related("topic")
                .order_by("order", "title", "id")
            )
            current_index = next(
                index for index, candidate in enumerate(task_list) if candidate.pk == task.pk
            )
            next_task = task_list[current_index + 1] if current_index + 1 < len(task_list) else None

    return render(
        request,
        "tasks/task_detail.html",
        {
            "course": course,
            "learning_set": learning_set,
            "topic": topic,
            "task": task,
            "is_correct": is_correct,
            "next_task": next_task,
            "reward_result": reward_result,
        },
    )
