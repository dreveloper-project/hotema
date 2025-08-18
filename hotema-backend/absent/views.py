# absent/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Absent

User = get_user_model()

class AbsentStatusView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()

        record = Absent.objects.filter(
            user=user,
            time_in__date=today
        ).order_by('-time_in').first()

        if record:
            if record.time_in and record.time_out is None:
                return Response({"status": "Absent Pulang"})
            elif record.time_in and record.time_out:
                return Response({"status": "Pekerjaan Sudah Selesai"})
        
        return Response({"status": "Absent Masuk"})


class CreateAbsentView(APIView):
    """
    Endpoint untuk mencatat absen masuk.
    - User hanya bisa absen masuk sekali per hari.
    - Jika sudah absen, kembalikan data absen yang sudah ada (bukan error).
    """

    def post(self, request):
        user_id = request.data.get("user_id")

        # Validasi user_id wajib ada
        if user_id is None:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validasi user ada
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        today = timezone.localdate()

        # Cek apakah user sudah absen masuk hari ini
        existing_absent = Absent.objects.filter(
            user=user,
            time_in__date=today
        ).first()

        if existing_absent:
            # ✅ Jangan balikin error, cukup info + data existing
            return Response({
                "message": "User sudah absen masuk hari ini",
                "absent_id": existing_absent.absent_id,
                "user": user.username,
                "time_in": existing_absent.time_in,
                "status": "IN_ALREADY"
            }, status=status.HTTP_200_OK)

        # ✅ Buat record baru kalau belum ada
        absent = Absent.objects.create(
            user=user,
            time_in=timezone.now()
        )

        return Response({
            "message": "Absent masuk berhasil dicatat",
            "absent_id": absent.absent_id,
            "user": user.username,
            "time_in": absent.time_in,
            "status": "IN_SUCCESS"
        }, status=status.HTTP_201_CREATED)
    
class AbsentOutView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()

        # cari record terakhir hari ini
        absent = Absent.objects.filter(
            user=user,
            time_in__date=today
        ).order_by("-time_in").first()

        if not absent:
            return Response({"error": "Belum ada absen masuk untuk hari ini"}, status=status.HTTP_400_BAD_REQUEST)

        if absent.time_out:
            return Response({"error": "User sudah absen pulang hari ini"}, status=status.HTTP_400_BAD_REQUEST)

        # update time_out
        absent.time_out = timezone.now()
        absent.save()

        return Response({
            "message": "Absent pulang berhasil dicatat",
            "absent_id": absent.absent_id,
            "user": user.username,
            "time_in": absent.time_in,
            "time_out": absent.time_out
        }, status=status.HTTP_200_OK)