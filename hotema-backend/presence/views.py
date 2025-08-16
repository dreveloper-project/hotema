# presence/api_views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from calendar import monthrange
from datetime import date

from .models import Shift, Schedule, PresenceRecord

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

class UserScheduleByMonthView(APIView):
    """
    Endpoint menerima POST dengan body:
    {
      "user_id": 2,
      "month": 8,
      "year": 2025
    }

    Response:
    {
      "date": ["2025-08-01", "2025-08-02", ...],
      "infobydate": ["Shift Pagi", "Libur", ...]
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        month = request.data.get("month")
        year = request.data.get("year")

        if not (user_id and month and year):
            return Response(
                {"error": "user_id, month, and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # pastikan user ada
        user = get_object_or_404(User, pk=user_id)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "month and year must be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # cari jumlah hari dalam bulan
        _, last_day = monthrange(year, month)

        dates = []
        info_by_date = []

        for day in range(1, last_day + 1):
            current_date = date(year, month, day)
            dates.append(current_date.isoformat())

            # cek schedule user
            schedule = Schedule.objects.filter(user=user, schedule_date=current_date).first()
            if schedule:
                if schedule.shift:  # ada shift
                    info_by_date.append(schedule.shift.shift_name)
                else:  # shift null → libur
                    info_by_date.append("Libur")
            else:
                info_by_date.append("Libur")

        return Response(
            {
                "date": dates,
                "infobydate": info_by_date
            },
            status=status.HTTP_200_OK
        )

class SetShiftView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        date_str = request.data.get("date")
        shift_id = request.data.get("shift_id")

        user = get_object_or_404(User, user_id=user_id)
        date_obj = date.fromisoformat(date_str)

        # kalau "libur" → jadikan None
        if shift_id == "libur" or shift_id is None:
            shift = None
        else:
            shift = get_object_or_404(Shift, shift_id=shift_id)

        schedule, created = Schedule.objects.update_or_create(
            user=user,
            schedule_date=date_obj,
            defaults={"shift": shift},
        )

        return Response(
            {"message": "Shift updated successfully", "libur": shift is None},
            status=status.HTTP_200_OK,
        )

