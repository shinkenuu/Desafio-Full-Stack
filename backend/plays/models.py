from django.db import models
from django.contrib.auth.models import User


from .settings import PLAY_FEE_PERCENT, PLAY_PRICE, PLAY_TOTAL_ACCENTS


class Attendee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Play(models.Model):
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
    attendee = models.ForeignKey(to=Attendee, on_delete=models.CASCADE, related_name='reservations', null=False)
    play = models.ForeignKey(to=Play, on_delete=models.CASCADE, related_name='reservations', null=False)

    class Meta:
        unique_together = (('attendee', 'play'), )
