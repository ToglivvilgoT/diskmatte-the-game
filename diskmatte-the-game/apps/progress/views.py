from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render

from .models import TaskCompletion, UserWallet


@login_required
def index(request):
    completions = TaskCompletion.objects.filter(user=request.user).select_related("task")
    wallet, _ = UserWallet.objects.get_or_create(user=request.user)
    leaderboard = list(
        get_user_model()
        .objects.annotate(
            total_disks_earned=Coalesce(F("userwallet__total"), Value(0))
        )
        .order_by("-total_disks_earned", "username")[:10]
    )
    highest_earned_disks = leaderboard[0].total_disks_earned if leaderboard else 0
    for player in leaderboard:
        player.earned_disk_percentage = (
            player.total_disks_earned * 100 // highest_earned_disks
            if highest_earned_disks
            else 0
        )
    return render(
        request,
        "progress/index.html",
        {
            "completions": completions,
            "solved_task_count": completions.count(),
            "wallet": wallet,
            "leaderboard": leaderboard,
        },
    )
