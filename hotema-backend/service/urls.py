from django.urls import path
from . import views
# service/create-record/
urlpatterns = [
    path('staff-by-date/', views.StaffAndRoomByDateAPIView.as_view(), name='staff-by-date'),
    path('create-record/', views.CreateRecordAPIView.as_view(), name='create-record'),
    path('records-with-task/', views.RecordWithTaskView.as_view(), name='records-with-task'),
    path('delete-record/', views.DeleteRecordView.as_view(), name='delete-record'),
    path('staff-task/', views.StaffTaskView.as_view(), name='staff-task'),
    path('start/', views.RecordStartView.as_view(), name='start'),
    path('complete/', views.RecordCompleteView.as_view(), name='complete'),
    path('task-monitoring/', views.SupervisorTaskView.as_view(), name='task-monitoring'),
    path('task/update-status/', views.UpdateTaskStatusView.as_view(), name='task-update-status'),
    
]
