from django.urls import path
from . import views

urlpatterns = [
    path('room-records/today/', views.RoomRecordTodayView.as_view(), name='room-records-today'),
    path('room-records/by-date/', views.RoomRecordByDateView.as_view(), name='room-records-by-date'),
    path('create/', views.RoomCreateView.as_view(), name='room-create'),
    path('occupancy-table/view/', views.OccupancyTableView.as_view(), name='occupancy-table-view'),
    path('get/all/', views.GetAllRoomView.as_view(), name='get-all-room'),
    path('add-occupancy/', views.AddOccupancyDataView.as_view(), name='add-occupancy'),
    path('delete-occupancy/', views.DeleteOccupancyView.as_view(), name='delete-occupancy'),
]
