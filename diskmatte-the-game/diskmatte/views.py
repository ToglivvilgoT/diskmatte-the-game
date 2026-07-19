from django.shortcuts import render


def home(request):
    apps = [
        {"name": "Accounts", "url": "/accounts/"},
        {"name": "Courses", "url": "/courses/"},
        {"name": "Tasks", "url": "/tasks/"},
        {"name": "Progress", "url": "/progress/"},
        {"name": "Leaderboard", "url": "/leaderboard/"},
    ]
    return render(request, "home.html", {"apps": apps})
