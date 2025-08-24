# service/api_views.py
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse
from django.views import View
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
                "staff": record.user.fullname if record.user else None,  # lebih aman
                "supervisor": task_monitor.user.fullname if (task_monitor and task_monitor.user) else None,
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
        records = Record.objects.filter(user_id=user_id).select_related("room")

        result = []
        for record in records:
            # Ambil task monitoring terkait record
            task_monitorings = TaskMonitoring.objects.filter(record=record)

            if task_monitorings.exists():
                for tm in task_monitorings:
                    # Skip kalau status = aprooved
                    if tm.tm_status and tm.tm_status.lower() == "aprooved":
                        continue
                    result.append({
                        "record_id": record.record_id,
                        "room_id": record.room_id,
                        "room_name": record.room.room_name,
                        "date": record.date,   # tambahkan date
                        "record_start": record.record_start,
                        "record_complete": record.record_complete,
                        "tm_user": tm.user.username if tm.user else None,  # <-- cek None
                        "tm_status": tm.tm_status
                    })
            else:
                # Jika tidak ada task monitoring
                result.append({
                    "record_id": record.record_id,
                    "room_id": record.room_id,
                    "room_name": record.room.room_name,
                    "date": record.date,   # tambahkan date
                    "record_start": record.record_start,
                    "record_complete": record.record_complete,
                    "tm_user": None,
                    "tm_status": None
                })

        return Response(result, status=status.HTTP_200_OK)



class RecordStartView(APIView):
    def post(self, request, *args, **kwargs):
        record_id = request.data.get("record_id")
        if not record_id:
            return Response({"error": "record_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Record.objects.get(record_id=record_id)
        except Record.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        # isi waktu mulai dengan waktu sekarang
        record.record_start = timezone.now().time()
        record.save(update_fields=["record_start"])

        return Response({
            "message": "Record start updated successfully",
            "record_id": record.record_id,
            "record_start": record.record_start
        }, status=status.HTTP_200_OK)


class RecordCompleteView(APIView):
    def post(self, request):
        record_id = request.data.get("record_id")
        if not record_id:
            return Response({"error": "record_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Record.objects.get(pk=record_id)
        except Record.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        # isi record_complete
        record.record_complete = now()
        record.save()

        # buat task monitoring otomatis
        TaskMonitoring.objects.create(
            user=None,              # belum di-QC
            record=record,          # relasi ke record
            tm_status="Uncheck"     # default status QC
        )

        return Response({
            "message": "Record marked as completed and task monitoring created.",
            "record_id": record.record_id,
            "record_complete": record.record_complete,
        }, status=status.HTTP_200_OK)
    


class SupervisorTaskView(View):
    def get(self, request):
        # ambil semua task dengan status "Uncheck" atau "Unaprooved"
        tasks = TaskMonitoring.objects.filter(tm_status__in=["Uncheck", "Unaprooved"]).select_related("record__room")

        data = []
        for task in tasks:
            data.append({
                "tm_id": task.tm_id,
                "tm_status": task.tm_status,
                "record_id": task.record.record_id,
                "room_id": task.record.room.room_id,
                "room_name": task.record.room.room_name,
                "user_id": task.record.user.user_id,
                "username": task.record.user.fullname,
                "date": task.record.date,
            })

        return JsonResponse(data, safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTaskStatusView(APIView):
    def post(self, request):
        try:
            tm_id = request.data.get("tm_id")
            status_value = request.data.get("status")

            if not tm_id or not status_value:
                return Response(
                    {"error": "tm_id dan status diperlukan"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if status_value not in ["Approved", "Unapproved"]:
                return Response(
                    {"error": "Status harus 'Approved' atau 'Unapproved'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            task = TaskMonitoring.objects.filter(tm_id=tm_id).first()
            if not task:
                return Response(
                    {"error": "Task tidak ditemukan"},
                    status=status.HTTP_404_NOT_FOUND
                )

            task.tm_status = status_value
            task.save()

            return Response({
                "message": f"Task {tm_id} berhasil diupdate ke status {status_value}",
                "tm_id": task.tm_id,
                "tm_status": task.tm_status
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)