# presence/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from calendar import monthrange
from datetime import date

from .models import Shift, Schedule

User = get_user_model()


class ShiftListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        shifts = Shift.objects.all().values("shift_id", "shift_name", "shift_start", "shift_stop")
        return Response(shifts)


class ShiftUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, shift_id):
        shift = get_object_or_404(Shift, pk=shift_id)

        # hanya update jam mulai dan jam selesai
        if "shift_start" in request.data:
            shift.shift_start = request.data["shift_start"]

        if "shift_stop" in request.data:
            shift.shift_stop = request.data["shift_stop"]

        shift.save()
        return Response(
            {"message": "Shift updated successfully"},
            status=status.HTTP_200_OK
        )


class PresenceView(APIView):
    """
    Ambil semua schedule user dalam bulan tertentu.
    Output: { 1: "Shift Pagi", 2: "Libur", ... }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            month = int(request.GET.get("month"))
            year = int(request.GET.get("year"))
        except (TypeError, ValueError):
            return Response({"error": "month dan year wajib dikirim"}, status=status.HTTP_400_BAD_REQUEST)

        # Hitung jumlah hari dalam bulan
        days_in_month = monthrange(year, month)[1]

        # Ambil semua schedule user di bulan tersebut
        schedules = Schedule.objects.filter(
            user_id=user_id,
            schedule_date__year=year,
            schedule_date__month=month
        ).select_related("shift")

        # Buat mapping {day: shift_name}
        schedule_map = {s.schedule_date.day: s.shift.shift_name for s in schedules}

        # Isi semua hari dengan shift/libur
        data = {}
        for day in range(1, days_in_month + 1):
            data[day] = schedule_map.get(day, "Libur")

        return Response(data, status=status.HTTP_200_OK)

class SetScheduleView(APIView):
    """
    Set atau update shift untuk user pada tanggal tertentu.
    Input: { "user_id": 1, "day": 3, "month": 8, "year": 2025, "shift": "Shift Pagi" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = int(request.data.get("user_id"))
            day = int(request.data.get("day"))
            month = int(request.data.get("month"))
            year = int(request.data.get("year"))
            shift_name = request.data.get("shift")
        except (TypeError, ValueError):
            return Response({"error": "user_id, day, month, year, dan shift wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)
        shift = get_object_or_404(Shift, shift_name=shift_name)

        schedule_date = date(year, month, day)

        schedule, created = Schedule.objects.update_or_create(
            user=user,
            schedule_date=schedule_date,
            defaults={"shift": shift}
        )

        return Response(
            {"message": "Schedule saved", "day": day, "shift": shift.shift_name},
            status=status.HTTP_200_OK
        )


class DeleteScheduleView(APIView):
    """
    Hapus shift pada tanggal tertentu → otomatis jadi Libur di frontend.
    Input: { "user_id": 1, "day": 3, "month": 8, "year": 2025 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = int(request.data.get("user_id"))
            day = int(request.data.get("day"))
            month = int(request.data.get("month"))
            year = int(request.data.get("year"))
        except (TypeError, ValueError):
            return Response({"error": "user_id, day, month, year wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

        schedule_date = date(year, month, day)
        schedule = Schedule.objects.filter(user_id=user_id, schedule_date=schedule_date)

        if schedule.exists():
            schedule.delete()
            return Response({"message": "Schedule deleted, now Libur"}, status=status.HTTP_200_OK)
        return Response({"message": "No schedule found for this date"}, status=status.HTTP_404_NOT_FOUND)
