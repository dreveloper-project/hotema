from django.urls import path
from . import views

urlpatterns = [
    path("shifts/lists/", views.ShiftListView.as_view(), name="shift-list"),
    path('shifts/<int:shift_id>/update/', views.ShiftUpdateView.as_view(), name="shift-update"),
    path('user-schedule/', views.UserScheduleByMonthView.as_view(), name="user-schedule"),
    path('set-shift/', views.SetShiftView.as_view(), name="set-shift"),
]