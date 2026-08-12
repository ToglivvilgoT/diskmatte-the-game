from django.urls import path

from .views import chapter_detail, course_detail, course_list

app_name = 'courses'

urlpatterns = [
    path('', course_list, name='course-list'),
    path('<slug:slug>/', course_detail, name='course-detail'),
    path('<slug:course_slug>/<slug:learning_set_slug>/<slug:slug>/', chapter_detail, name='chapter-detail'),
]
