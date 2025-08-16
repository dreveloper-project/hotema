from django.urls import path
from . import views

urlpatterns = [
    path("shifts/lists/", views.ShiftListView.as_view(), name="shift-list"),
    path('shifts/<int:shift_id>/update/', views.ShiftUpdateView.as_view(), name="shift-update"),
    path("<int:user_id>/", views.PresenceView.as_view(), name="presence"),
    path("set/", views.SetScheduleView.as_view(), name="set_schedule"),
    path("delete/", views.DeleteScheduleView.as_view(), name="delete_schedule"),
]