from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import RoomRecord
from django.utils import timezone
from django.core import serializers
from django.utils.dateparse import parse_date
import json
from .models import Room
from rest_framework import status

class RoomRecordTodayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        room_records = RoomRecord.objects.filter(date=today)
        
        # Serialize the data
        data = []
        for record in room_records:
            data.append({
                'rr_id': record.rr_id,
                'room_id': record.room.room_id,
                'room_name': record.room.room_name,
                'guest_status': record.guest_status,
                'cleanliness_status': record.cleanliness_status,
                'date': record.date
            })
        
        return Response(data)
    


class RoomRecordByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        print(date_str)
        if not date_str:
            return Response({"error": "Parameter 'date' wajib diisi (format: YYYY-MM-DD)."}, status=400)

        date_obj = parse_date(date_str)
        if not date_obj:
            return Response({"error": "Format tanggal tidak valid. Gunakan YYYY-MM-DD."}, status=400)

        room_records = RoomRecord.objects.filter(date=date_obj)

        if not room_records.exists():
            return Response({"error": "Data tidak ditemukan pada tanggal tersebut."}, status=404)

        data = []
        for record in room_records:
            data.append({
                'rr_id': record.rr_id,
                'room_id': record.room.room_id,
                'room_name': record.room.room_name,
                'guest_status': record.guest_status,
                'cleanliness_status': record.cleanliness_status,
                'date': record.date
            })

        return Response(data)

class RoomCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nama_kamar = request.data.get('nama_kamar')
        tipe_kamar = request.data.get('tipe_kamar')

        # Validasi sederhana
        if not nama_kamar or not tipe_kamar:
            return Response(
                {"error": "Field 'nama_kamar' dan 'tipe_kamar' wajib diisi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simpan ke database
        room = Room.objects.create(
            room_name=nama_kamar,
            room_type=tipe_kamar
        )

        return Response({
            "message": "Kamar berhasil ditambahkan.",
            "room_id": room.room_id,
            "room_name": room.room_name,
            "room_type": room.room_type
        }, status=status.HTTP_201_CREATED)