from apps.courses.models import Course


def navigation_course(request):
    return {"navigation_course": Course.objects.filter(is_active=True).first()}
