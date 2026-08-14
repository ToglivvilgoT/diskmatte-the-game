from django.urls import path

from .views import task_detail

app_name = 'tasks'

urlpatterns = [
    path('<slug:course_slug>/<slug:learning_set_slug>/<slug:topic_slug>/<slug:slug>/', task_detail, name='task-detail'),
]
