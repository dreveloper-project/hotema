# service/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from presence.models import Schedule
from room.models import Room
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from room.models import Room
from customuser.models import CustomUser
from .models import Record, TaskMonitoring
User = get_user_model()


class StaffAndRoomByDateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        date_str = request.data.get("date")  # ambil date dari body JSON
        if not date_str:
            return Response(
                {"error": "Parameter 'date' harus dikirim (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # parsing ke datetime, lalu majukan 1 hari
            date_obj = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
            date = date_obj.date()
        except ValueError:
            return Response(
                {"error": "Format tanggal harus YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ambil semua staff yang dijadwalkan di tanggal tsb
        schedules = Schedule.objects.filter(schedule_date=date).select_related("user", "shift")

        # ambil semua room
        rooms = Room.objects.all().values("room_id", "room_name")

        if schedules.exists():
            staff = [
                {
                    "user_id": s.user.user_id,
                    "full_name": getattr(s.user, "fullname", None) or s.user.username,
                }
                for s in schedules
            ]
            return Response(
                {
                    "date": str(date),   # pastikan string agar JSON valid
                    "staff": staff,
                    "rooms": list(rooms),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "date": str(date),
                    "message": "Tidak Ada Staff Yang Bertugas pada hari itu !",
                    "rooms": list(rooms),
                },
                status=status.HTTP_200_OK,
            )
        



class CreateRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        date_str = request.data.get("date")
        user_id = request.data.get("user_id")
        room_id = request.data.get("room_id")

        # validasi parameter
        if not date_str or not user_id or not room_id:
            return Response(
                {"error": "Parameter 'date', 'user_id', dan 'room_id' wajib dikirim"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # parsing date & majukan 1 hari
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
            date = date_obj.date()
        except ValueError:
            return Response(
                {"error": "Format tanggal harus YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # validasi user & room
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": f"User dengan id {user_id} tidak ditemukan"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": f"Room dengan id {room_id} tidak ditemukan"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # buat record baru
        record = Record.objects.create(
            user=user,
            room=room,
            date=date,
            record_start=None,
            record_complete=None,
        )

        return Response(
            {
                "message": "Record berhasil dibuat",
                "record": {
                    "record_id": record.record_id,
                    "user_id": record.user.user_id,
                    "room_id": record.room.room_id,
                    "date": str(record.date),
                    "record_start": record.record_start,
                    "record_complete": record.record_complete,
                },
            },
            status=status.HTTP_201_CREATED,
        )




# service/views.py
class RecordWithTaskView(APIView):
    def get(self, request, *args, **kwargs):
        records = Record.objects.select_related("room", "user").all()

        result = []
        for record in records:
            task_monitor = TaskMonitoring.objects.filter(record=record).select_related("user").first()

            result.append({
                "record_id": record.record_id,  
                "kamar": record.room.room_name,
                "jadwal": record.date.strftime("%Y-%m-%d"),
                "waktu_mulai": record.record_start.strftime("%H:%M:%S") if record.record_start else None,
                "waktu_selesai": record.record_complete.strftime("%H:%M:%S") if record.record_complete else None,
                "staff": record.user.fullname,
                "supervisor": task_monitor.user.fullname if task_monitor else None,
                "qc_status": task_monitor.tm_status if task_monitor else None,
            })

        return Response(result, status=status.HTTP_200_OK)
    

class DeleteRecordView(APIView):


    def post(self, request, *args, **kwargs):
        record_id = request.data.get("record_id")
        if not record_id:
            return Response({"error": "record_id wajib dikirim"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Record.objects.get(pk=record_id)
            record.delete()
            return Response({"message": f"Record {record_id} berhasil dihapus"}, status=status.HTTP_200_OK)
        except Record.DoesNotExist:
            return Response({"error": "Record tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)


# part milik staff
# 
# 


class StaffTaskView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ambil semua record untuk user_id
        records = Record.objects.filter(user_id=user_id)

        result = []
        for record in records:
            # Ambil task monitoring terkait record
            task_monitorings = TaskMonitoring.objects.filter(record=record)

            if task_monitorings.exists():
                for tm in task_monitorings:
                    # Skip kalau status = aprooved
                    if tm.tm_status.lower() == "aprooved":
                        continue
                    result.append({
                        "record_id": record.record_id,
                        "room_id": record.room_id,
                        "record_start": record.record_start,
                        "record_complete": record.record_complete,
                        "tm_user": tm.user.username,
                        "tm_status": tm.tm_status
                    })
            else:
                # Jika tidak ada task monitoring
                result.append({
                    "record_id": record.record_id,
                    "room_id": record.room_id,
                    "record_start": record.record_start,
                    "record_complete": record.record_complete,
                    "tm_user": None,
                    "tm_status": None
                })

        return Response(result, status=status.HTTP_200_OK)
