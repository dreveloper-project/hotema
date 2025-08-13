from django.urls import path
from . import views

urlpatterns = [
    path('users-without-role/', views.UsersWithoutRoleView.as_view(), name='users-without-role'),
    path('update-role/', views.UpdateUserRoleView.as_view(), name='update-user-role'),
    path('users-by-role/', views.UsersByRoleView.as_view(), name='users-by-role')
]
