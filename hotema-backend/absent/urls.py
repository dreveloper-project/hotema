from django.urls import path
from . import views

urlpatterns = [
        path('status/', views.AbsentStatusView.as_view(), name='absent-status'),
        path('create/', views.CreateAbsentView.as_view(), name='create-absent'),
        path('out/', views.AbsentOutView.as_view(), name='absent-out'),
]
