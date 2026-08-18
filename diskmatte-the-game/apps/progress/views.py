from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import F, Value, Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render

from apps.courses.models import Course
from apps.tasks.models import Task
from .models import TaskCompletion, UserWallet


@login_required
def index(request):
    wallet, _ = UserWallet.objects.get_or_create(user=request.user)
    leaderboard = list(
        get_user_model()
        .objects.annotate(
            total_disks_earned=Coalesce(F("userwallet__total"), Value(0))
        )
        .select_related("useravatar__equipped_skin")
        .order_by("-total_disks_earned", "username")[:10]
    )
    highest_earned_disks = leaderboard[0].total_disks_earned if leaderboard else 0
    for player in leaderboard:
        player.earned_disk_percentage = (
            player.total_disks_earned * 100 // highest_earned_disks
            if highest_earned_disks
            else 0
        )
    
    # Calculate progress on the existing chapter
    chapter = Course.objects.first()
    chapter_progress = None
    if chapter:
        total_tasks = Task.objects.filter(learning_set__course=chapter).count()
        completed_tasks = TaskCompletion.objects.filter(
            user=request.user,
            task__learning_set__course=chapter
        ).count()
        chapter_progress = {
            "name": chapter.name,
            "completed": completed_tasks,
            "total": total_tasks,
            "percentage": (completed_tasks * 100 // total_tasks) if total_tasks else 0,
        }
    
    return render(
        request,
        "progress/index.html",
        {
            "wallet": wallet,
            "leaderboard": leaderboard,
            "chapter_progress": chapter_progress,
        },
    )
