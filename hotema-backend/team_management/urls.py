from django.urls import path
from . import views

urlpatterns = [
    path('users-without-role/', views.UsersWithoutRoleView.as_view(), name='users-without-role'),
    path('update-role/', views.UpdateUserRoleView.as_view(), name='update-user-role'),
    path('users-by-role/', views.UsersByRoleView.as_view(), name='users-by-role'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<int:user_id>/delete/', views.DeleteUserView.as_view(), name='users-delete'),
    path('users/<int:user_id>/update-role/', views.UpdateUserRoleByIdView.as_view(), name='update-user-role-by-id'),
]
