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
from datetime import timedelta
from django.db.models import Q
from datetime import datetime, timedelta

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
    
class OccupancyTableView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get and validate date parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response(
                {"error": " 'start_date' dan 'end_date'  are required (format: YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            
            if not start_date or not end_date:
                raise ValueError("Invalid date format")
                
            if start_date > end_date:
                return Response(
                    {"error": "Start date cannot be after end date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate date range for headers
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        # Get all rooms ordered by name
        rooms = Room.objects.all().order_by('room_name')
        
        # Get all room records within the date range
        room_records = RoomRecord.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related('room')
        
        # Create a mapping of room records for quick lookup
        records_map = {}
        for record in room_records:
            room_id = record.room.room_id
            if room_id not in records_map:
                records_map[room_id] = {}
            
            # Convert detailed status to simplified IN/OUT format
            status_mapping = {
                "Checked In": "IN",
                "Checked Out": "OUT",
                "Occupied": "IN",
                "Reserved": "IN",
                "Vacant": "OUT"
            }
            simplified_status = status_mapping.get(record.guest_status, None)
            records_map[room_id][record.date] = simplified_status
        
        # Build the response data structure
        headers = [date.strftime('%d %B') for date in date_range]  # e.g., "03 Agustus"

        rows = []
        for room in rooms:
            room_data = {
                'id': str(room.room_name) if room.room_name else f"Room {room.room_id}",
                'days': []
            }
            
            # Populate status for each day in the date range
            for date in date_range:
                status = records_map.get(room.room_id, {}).get(date, None)
                room_data['days'].append({'status': status})
            
            rows.append(room_data)

        return Response({
            'tableData': {
                'headers': headers,
                'rows': rows
            }
        })
class GetAllRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all().order_by('room_name')
        room_names = [room.room_name for room in rooms if room.room_name]

        return Response({
            'rooms': room_names
        })

class AddOccupancyDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_name = request.data.get('room_name')
        check_in_date = request.data.get('check_in_date')
        check_out_date = request.data.get('check_out_date')
        
        if not all([room_name, check_in_date, check_out_date]):
            return Response(
                {"error": "room_name, check_in_date, and check_out_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Parse dates dan majukan 1 hari
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date() + timedelta(days=1)
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date() + timedelta(days=1)
            
            if check_in >= check_out:
                return Response(
                    {"error": "Check-out date must be after check-in date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Ambil room berdasarkan nama
            try:
                room = Room.objects.get(room_name=room_name)
            except Room.DoesNotExist:
                return Response(
                    {"error": f"Room '{room_name}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            current_date = check_in
            records_created = []
            
            # Buat record dari check-in sampai sebelum check-out
            while current_date < check_out:
                RoomRecord.objects.filter(
                    room=room,
                    date=current_date
                ).delete()
                
                new_record = RoomRecord.objects.create(
                    room=room,
                    guest_status="Checked In",
                    cleanliness_status="Occupied",
                    date=current_date
                )
                records_created.append({
                    'rr_id': new_record.rr_id,
                    'room_name': room.room_name,
                    'date': str(current_date),
                    'guest_status': new_record.guest_status,
                    'action': 'created_or_overwritten'
                })
                
                current_date += timedelta(days=1)
            
            # Buat record checkout
            RoomRecord.objects.filter(
                room=room,
                date=check_out
            ).delete()
            
            checkout_record = RoomRecord.objects.create(
                room=room,
                guest_status="Checked Out",
                cleanliness_status="Vacant",
                date=check_out
            )
            records_created.append({
                'rr_id': checkout_record.rr_id,
                'room_name': room.room_name,
                'date': str(check_out),
                'guest_status': checkout_record.guest_status,
                'action': 'created_or_overwritten'
            })
            
            return Response({
                'message': 'Occupancy data added successfully (dates shifted +1 day)',
                'records_created': len(records_created),
                'details': records_created
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {"error": f"Invalid date format: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
