from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("courses/", include("apps.courses.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("progress/", include("apps.progress.urls")),
    path("leaderboard/", include("apps.leaderboard.urls")),
    path("avatar/", include("apps.cosmetics.urls")),
]