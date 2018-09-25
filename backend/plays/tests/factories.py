from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory import SubFactory, Sequence

from ..models import Attendee, Play, Reservation


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda x: 'Test User #' + str(x))
    password = 'raduguiF1re'
    email = Sequence(lambda x: 'test.user' + str(x) + '@host.com')


class AttendeeFactory(DjangoModelFactory):
    class Meta:
        model = Attendee

    user = SubFactory(UserFactory)


class PlayFactory(DjangoModelFactory):
    class Meta:
        model = Play

    name = Sequence(lambda x: 'Play #' + str(x))


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    attendee = SubFactory(AttendeeFactory)
    play = SubFactory(PlayFactory)
