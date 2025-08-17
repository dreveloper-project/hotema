from django.db import models
from django.conf import settings


class Absent(models.Model):
    absent_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='absents'
    )
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'absent'
        verbose_name = 'Absent'
        verbose_name_plural = 'Absents'

    def __str__(self):
        return f"{self.user.username} - In: {self.time_in}, Out: {self.time_out}"


