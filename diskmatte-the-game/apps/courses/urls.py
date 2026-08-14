from django.urls import path

from .views import course_detail, course_list, topic_detail

app_name = 'courses'

urlpatterns = [
    path('', course_list, name='course-list'),
    path('<slug:slug>/', course_detail, name='course-detail'),
    path('<slug:course_slug>/<slug:learning_set_slug>/<slug:topic_slug>/', topic_detail, name='topic-detail'),
]
