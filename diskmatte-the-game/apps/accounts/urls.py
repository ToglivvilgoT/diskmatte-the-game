from django.urls import path

from .views import index, login_view, logout_view, register

app_name = 'accounts'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
