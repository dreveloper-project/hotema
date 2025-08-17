from django.contrib import admin
from .models import Record, TaskMonitoring

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'room', 'user', 'date', 'record_start', 'record_complete')
    list_filter = ('date', 'room', 'user')
    search_fields = ('room__room_name', 'user__username', 'user__email')
    ordering = ('-date', '-record_start')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('room', 'user', 'date')
        }),
        ('Time Information', {
            'fields': ('record_start', 'record_complete')
        }),
    )

@admin.register(TaskMonitoring)
class TaskMonitoringAdmin(admin.ModelAdmin):
    list_display = ('tm_id', 'user', 'record', 'tm_status')
    list_filter = ('tm_status', 'user', 'record__date')
    search_fields = ('user__username', 'user__email', 'record__room__room_name', 'tm_status')
    ordering = ('-tm_id',)
    
    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'record', 'tm_status')
        }),
    )
