# presence/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Shift
from rest_framework import status
from django.shortcuts import get_object_or_404

class ShiftListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        shifts = Shift.objects.all().values("shift_name", "shift_start", "shift_stop")
        return Response(shifts)
class ShiftUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, shift_id):
        shift = get_object_or_404(Shift, pk=shift_id)
        shift.shift_name = request.data.get("shift_name", shift.shift_name)
        shift.shift_start = request.data.get("shift_start", shift.shift_start)
        shift.shift_stop = request.data.get("shift_stop", shift.shift_stop)
        shift.save()
        return Response({"message": "Shift updated successfully"}, status=status.HTTP_200_OK)