from rest_framework import serializers
from .models import Record, TaskMonitoring
from customuser.models import CustomUser
from room.models import Room

class RecordSerializer(serializers.ModelSerializer):
    """Serializer for Record model."""
    
    room_name = serializers.CharField(source='room.room_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Record
        fields = [
            'record_id',
            'room',
            'room_name',
            'user',
            'username',
            'user_email',
            'date',
            'record_start',
            'record_complete'
        ]
        read_only_fields = ['record_id']

    def validate(self, data):
        """Validate that record_complete is after record_start."""
        if data.get('record_start') and data.get('record_complete'):
            if data['record_complete'] <= data['record_start']:
                raise serializers.ValidationError(
                    "Record complete time must be after record start time."
                )
        return data


class TaskMonitoringSerializer(serializers.ModelSerializer):
    """Serializer for TaskMonitoring model."""
    
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    record_info = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskMonitoring
        fields = [
            'tm_id',
            'user',
            'username',
            'user_email',
            'record',
            'record_info',
            'tm_status'
        ]
        read_only_fields = ['tm_id']
    
    def get_record_info(self, obj):
        """Get formatted record information."""
        return {
            'record_id': obj.record.record_id,
            'room_name': obj.record.room.room_name,
            'date': obj.record.date,
            'start_time': obj.record.record_start,
            'complete_time': obj.record.record_complete
        }


class RecordSummarySerializer(serializers.ModelSerializer):
    """Summary serializer for Record model (for nested representations)."""
    
    class Meta:
        model = Record
        fields = ['record_id', 'date', 'record_start', 'record_complete']


class TaskMonitoringDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for TaskMonitoring with nested record data."""
    
    record_detail = RecordSummarySerializer(source='record', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TaskMonitoring
        fields = [
            'tm_id',
            'user',
            'username',
            'record',
            'record_detail',
            'tm_status'
        ]
