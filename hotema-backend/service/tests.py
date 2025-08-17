from django.test import TestCase
from django.contrib.auth import get_user_model
from room.models import Room
from .models import Record, TaskMonitoring
from datetime import date, time

User = get_user_model()

class ServiceModelsTestCase(TestCase):
    """Test cases for service models."""
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            fullname='Test User',
            password='testpass123'
        )
        
        # Create test room
        self.room = Room.objects.create(
            room_name='Test Room',
            room_type='Test Type'
        )
        
        # Create test record
        self.record = Record.objects.create(
            room=self.room,
            user=self.user,
            date=date.today(),
            record_start=time(9, 0, 0),
            record_complete=time(17, 0, 0)
        )
        
        # Create test task monitoring
        self.task_monitoring = TaskMonitoring.objects.create(
            user=self.user,
            record=self.record,
            tm_status='in_progress'
        )
    
    def test_record_creation(self):
        """Test record creation."""
        self.assertEqual(self.record.room, self.room)
        self.assertEqual(self.record.user, self.user)
        self.assertEqual(self.record.date, date.today())
        self.assertEqual(str(self.record), f"Record {self.record.record_id} - Room Test Room - User testuser - {date.today()}")
    
    def test_task_monitoring_creation(self):
        """Test task monitoring creation."""
        self.assertEqual(self.task_monitoring.user, self.user)
        self.assertEqual(self.task_monitoring.record, self.record)
        self.assertEqual(self.task_monitoring.tm_status, 'in_progress')
        self.assertEqual(str(self.task_monitoring), f"Task {self.task_monitoring.tm_id} - Status: in_progress - Record {self.record.record_id}")
    
    def test_record_foreign_keys(self):
        """Test record foreign key relationships."""
        self.assertEqual(self.record.room.room_name, 'Test Room')
        self.assertEqual(self.record.user.username, 'testuser')
    
    def test_task_monitoring_foreign_keys(self):
        """Test task monitoring foreign key relationships."""
        self.assertEqual(self.task_monitoring.record.room.room_name, 'Test Room')
        self.assertEqual(self.task_monitoring.user.username, 'testuser')


class ServiceAPITestCase(TestCase):
    """Test cases for service API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            fullname='Test User',
            password='testpass123'
        )
        
        self.room = Room.objects.create(
            room_name='Test Room',
            room_type='Test Type'
        )
        
        self.record = Record.objects.create(
            room=self.room,
            user=self.user,
            date=date.today(),
            record_start=time(9, 0, 0),
            record_complete=time(17, 0, 0)
        )
        
        self.task_monitoring = TaskMonitoring.objects.create(
            user=self.user,
            record=self.record,
            tm_status='in_progress'
        )
    
    def test_record_list(self):
        """Test record list endpoint."""
        from rest_framework.test import APIClient
        from rest_framework_simplejwt.tokens import RefreshToken
        
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = client.get('/api/service/api/records/')
        self.assertEqual(response.status_code, 200)
    
    def test_task_monitoring_list(self):
        """Test task monitoring list endpoint."""
        from rest_framework.test import APIClient
        from rest_framework_simplejwt.tokens import RefreshToken
        
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = client.get('/api/service/api/task-monitorings/')
        self.assertEqual(response.status_code, 200)
