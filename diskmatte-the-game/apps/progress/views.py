from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TaskCompletion


@login_required
def index(request):
    completions = TaskCompletion.objects.filter(user=request.user).select_related("task")
    return render(
        request,
        "progress/index.html",
        {"completions": completions, "solved_task_count": completions.count()},
    )
