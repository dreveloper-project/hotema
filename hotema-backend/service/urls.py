from django.urls import path
from . import views
# service/create-record/
urlpatterns = [
    path('staff-by-date/', views.StaffAndRoomByDateAPIView.as_view(), name='staff-by-date'),
    path('create-record/', views.CreateRecordAPIView.as_view(), name='create-record'),
    
]
