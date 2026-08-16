from django.urls import path

from .views import course_detail, learning_set_detail, topic_detail

app_name = 'courses'

urlpatterns = [
    path('<slug:slug>/', course_detail, name='course-detail'),
    path('<slug:course_slug>/<slug:slug>/', learning_set_detail, name='learning-set-detail'),
    path('<slug:course_slug>/<slug:learning_set_slug>/<slug:topic_slug>/', topic_detail, name='topic-detail'),
]
