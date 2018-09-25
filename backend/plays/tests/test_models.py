from django.db.utils import IntegrityError
from django.test.testcases import TestCase

from ..models import Attendee, Play, Reservation
from ..settings import PLAY_FEE_PERCENT, PLAY_PRICE, PLAY_TOTAL_ACCENTS

from .factories import AttendeeFactory, PlayFactory, ReservationFactory


class AttendeeTestCase(TestCase):
    def test_persistence(self):
        attendee = AttendeeFactory()
        persisted_attendee = Attendee.objects.get(id=attendee.id)

        self.assertEqual(attendee.user.id, persisted_attendee.user.id)


class PlayTestCase(TestCase):
    def test_persistence(self):
        play = PlayFactory()
        persisted_play = Play.objects.get(id=play.id)

        self.assertEqual(persisted_play.name, play.name)
        self.assertEqual(persisted_play.fee, PLAY_FEE_PERCENT)
        self.assertEqual(persisted_play.price, PLAY_PRICE)
        self.assertEqual(persisted_play.total_accents, PLAY_TOTAL_ACCENTS)

    def test_property_amount_of_available_accents(self):
        play = PlayFactory()

        expected_amount_of_available_accents = play.total_accents
        self.assertEqual(play.amount_of_available_accents, expected_amount_of_available_accents)

        # First reservation
        ReservationFactory(play=play)
        expected_amount_of_available_accents = play.total_accents - 1
        self.assertEqual(play.amount_of_available_accents, expected_amount_of_available_accents)

        # Second reservation
        ReservationFactory(play=play)
        expected_amount_of_available_accents = play.total_accents - 2
        self.assertEqual(play.amount_of_available_accents, expected_amount_of_available_accents)

    def test_property_revenue(self):
        price = 11.1
        play = PlayFactory(price=price)

        expected_revenue = 0.
        self.assertEqual(play.revenue, expected_revenue)

        # Increasing revenue

        first_reservation = ReservationFactory(play=play)
        expected_revenue = price
        self.assertEqual(play.revenue, expected_revenue)

        second_reservation = ReservationFactory(play=play)
        expected_revenue = price * 2
        self.assertEqual(play.revenue, expected_revenue)

        # Decreasing revenue

        Reservation.objects.get(id=first_reservation.id).delete()
        expected_revenue = price
        self.assertEqual(play.revenue, expected_revenue)

        Reservation.objects.get(id=second_reservation.id).delete()
        expected_revenue = 0.
        self.assertEqual(play.revenue, expected_revenue)

    def test_property_total_fee(self):
        price = 10.
        fee = 0.1
        play = PlayFactory(price=price, fee=fee)

        expected_total_fee = 0.
        self.assertEqual(play.total_fee, expected_total_fee)

        # Increasing revenue

        first_reservation = ReservationFactory(play=play)
        expected_total_fee = price * fee
        self.assertEqual(play.total_fee, expected_total_fee)

        second_reservation = ReservationFactory(play=play)
        expected_total_fee = price * 2 * fee
        self.assertEqual(play.total_fee, expected_total_fee)

        # Decreasing revenue

        Reservation.objects.get(id=first_reservation.id).delete()
        expected_total_fee = price * fee
        self.assertEqual(play.total_fee, expected_total_fee)

        Reservation.objects.get(id=second_reservation.id).delete()
        expected_total_fee = 0.
        self.assertEqual(play.total_fee, expected_total_fee)


class ReservationTestCase(TestCase):
    def test_persistence(self):
        reservation = ReservationFactory()
        persisted_reservation = Reservation.objects.get(id=reservation.id)

        self.assertEqual(reservation.attendee.id, persisted_reservation.attendee.id)
        self.assertEqual(reservation.play.id, persisted_reservation.play.id)

    def test_attendee_cant_have_more_than_one_reservation_for_the_same_play(self):
        attendee = AttendeeFactory()
        play = PlayFactory()

        Reservation.objects.create(attendee=attendee, play=play)

        expected_error_message = 'UNIQUE constraint failed: plays_reservation.attendee_id, plays_reservation.play_id'

        with self.assertRaisesRegex(IntegrityError, expected_error_message):
            Reservation.objects.create(attendee=attendee, play=play)
