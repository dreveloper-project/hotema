from django.urls import path
from . import views

urlpatterns = [
    path('room-records/today/', views.RoomRecordTodayView.as_view(), name='room-records-today'),
    path('room-records/by-date/', views.RoomRecordByDateView.as_view(), name='room-records-by-date'),
]
