# Service App

This Django app provides functionality for managing room records and task monitoring.

## Models

### Record
Stores room usage records with start and complete times.

**Fields:**
- `record_id`: Primary key (BigAutoField)
- `room`: ForeignKey to Room model
- `user`: ForeignKey to CustomUser model
- `date`: DateField (yyyy-mm-dd format)
- `record_start`: TimeField
- `record_complete`: TimeField

### TaskMonitoring
Monitors task status for records.

**Fields:**
- `tm_id`: Primary key (BigAutoField)
- `user`: ForeignKey to CustomUser model
- `record`: ForeignKey to Record model
- `tm_status`: CharField (max_length=50)

## API Endpoints

### Records
- `GET /api/service/api/records/` - List all records
- `POST /api/service/api/records/` - Create new record
- `GET /api/service/api/records/{id}/` - Retrieve specific record
- `PUT /api/service/api/records/{id}/` - Update record
- `DELETE /api/service/api/records/{id}/` - Delete record
- `GET /api/service/api/records/{id}/task_monitorings/` - Get task monitorings for record

**Query Parameters:**
- `date`: Filter by specific date
- `start_date`: Filter by start date (inclusive)
- `end_date`: Filter by end date (inclusive)
- `room_name`: Filter by room name (contains)
- `username`: Filter by username (contains)

### Task Monitorings
- `GET /api/service/api/task-monitorings/` - List all task monitorings
- `POST /api/service/api/task-monitorings/` - Create new task monitoring
- `GET /api/service/api/task-monitorings/{id}/` - Retrieve specific task monitoring
- `PUT /api/service/api/task-monitorings/{id}/` - Update task monitoring
- `DELETE /api/service/api/task-monitorings/{id}/` - Delete task monitoring
- `GET /api/service/api/task-monitorings/by_user/` - Get current user's task monitorings
- `GET /api/service/api/task-monitorings/status_summary/` - Get status summary

**Query Parameters:**
- `tm_status`: Filter by status
- `user`: Filter by user ID
- `record`: Filter by record ID
- `record_date`: Filter by record date
- `room_id`: Filter by room ID

## Usage Examples

### Creating a Record
```bash
curl -X POST http://localhost:8000/api/service/api/records/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "user": 1,
    "date": "2024-01-15",
    "record_start": "09:00:00",
    "record_complete": "17:00:00"
  }'
```

### Creating a Task Monitoring
```bash
curl -X POST http://localhost:8000/api/service/api/task-monitorings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "record": 1,
    "tm_status": "in_progress"
  }'
```

### Filtering Records
```bash
# Get records for a specific date
curl -X GET "http://localhost:8000/api/service/api/records/?date=2024-01-15" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get records for a date range
curl -X GET "http://localhost:8000/api/service/api/records/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Admin Interface
The models are registered in Django admin with custom list displays and filters:
- Records: Filter by date, room, user
- Task Monitorings: Filter by status, user, record date

## Testing
Run tests with:
```bash
python manage.py test service
