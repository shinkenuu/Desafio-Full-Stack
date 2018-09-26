from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from .settings import PLAY_FEE_PERCENT, PLAY_PRICE, PLAY_TOTAL_ACCENTS


class Attendee(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=False, related_name='attendee')


class Play(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    fee = models.FloatField(null=False, default=PLAY_FEE_PERCENT)
    price = models.FloatField(null=False, default=PLAY_PRICE)
    total_accents = models.IntegerField(null=False, default=PLAY_TOTAL_ACCENTS)

    @property
    def amount_of_available_accents(self):
        reservations = self.reservations.all()

        if reservations:
            return self.total_accents - len(reservations)

        return self.total_accents

    @property
    def revenue(self):
        reservations = self.reservations.all()

        if reservations:
            return self.price * len(reservations)

        return 0.

    @property
    def total_fee(self):
        return self.revenue * self.fee


class Reservation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    attendee = models.ForeignKey(to=Attendee, on_delete=models.CASCADE, related_name='reservations', null=False)
    play = models.ForeignKey(to=Play, on_delete=models.CASCADE, related_name='reservations', null=False)

    class Meta:
        unique_together = (('attendee', 'play'), )
