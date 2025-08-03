from django.db import models

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255, null=True, blank=True)
    room_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.room_name if self.room_name else f"Room {self.room_id}"

class RoomRecord(models.Model):
    rr_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='records')
    guest_status = models.CharField(max_length=255, null=True, blank=True)
    cleanliness_status = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Record {self.rr_id} for Room {self.room.room_id}"
