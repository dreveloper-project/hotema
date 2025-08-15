from django.contrib import admin
from .models import PresenceRecord, Shift, Schedule

# Register all models in Django Admin
admin.site.register(PresenceRecord)
admin.site.register(Shift)
admin.site.register(Schedule)
