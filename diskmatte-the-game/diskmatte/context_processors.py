from apps.courses.models import Course


def navigation_courses(request):
    return {"navigation_courses": Course.objects.filter(is_active=True)}
