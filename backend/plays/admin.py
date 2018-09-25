from django.contrib import admin

from .models import Attendee, Play, Reservation

admin.register(Attendee)
admin.register(Play)
admin.register(Reservation)
