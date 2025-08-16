from django.db import models
from django.conf import settings


class Shift(models.Model):
    shift_id = models.BigAutoField(primary_key=True)
    shift_name = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_stop = models.TimeField()

    def __str__(self):
        return f"{self.shift_name} ({self.shift_start} - {self.shift_stop})"


class Schedule(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    schedule_date = models.DateField()
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.schedule_date} ({self.shift.shift_name})"


class PresenceRecord(models.Model):
    presence_id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.date} (In: {self.time_in}, Out: {self.time_out})"
