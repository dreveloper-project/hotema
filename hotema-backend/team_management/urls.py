from django.urls import path
from . import views

urlpatterns = [
    path('users-without-role/', views.UsersWithoutRoleView.as_view(), name='users-without-role'),
]
