from django.db import models
from customuser.models import CustomUser
from room.models import Room

class Record(models.Model):
    """Model to store room records with start and complete times."""
    
    record_id = models.BigAutoField(primary_key=True)
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='service_records',
        db_column='room_id'
    )
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='service_records',
        db_column='user_id'
    )
    date = models.DateField()
    record_start = models.TimeField(null=True, blank=True)
    record_complete = models.TimeField(null=True, blank=True)
    class Meta:
        db_table = 'record'
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
    
    def __str__(self):
        return f"Record {self.record_id} - Room {self.room.room_name} - User {self.user.username} - {self.date}"

class TaskMonitoring(models.Model):
    """Model to monitor task status for records."""
    
    tm_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='task_monitorings',
        db_column='user_id',
        null=True,        # boleh NULL di database
        blank=True        # boleh kosong di form/admin
    )
    record = models.ForeignKey(
        Record, 
        on_delete=models.CASCADE, 
        related_name='task_monitorings',
        db_column='record_id'
    )
    tm_status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'task_monitoring'
        verbose_name = 'Task Monitoring'
        verbose_name_plural = 'Task Monitorings'
    
    def __str__(self):
        return f"Task {self.tm_id} - Status: {self.tm_status} - Record {self.record.record_id}"

