from django.contrib.auth.hashers import check_password
from django.test.testcases import TestCase
from rest_framework import status

from ..models import Attendee, Play, Reservation

from .factories import AttendeeFactory, PlayFactory, ReservationFactory


class AttendeeDetailViewTestCase(TestCase):
    def setUp(self):
        self.attendee = AttendeeFactory()
        self.noisy_attendee = AttendeeFactory()
        self.attendees_detail_url = '/api/attendees/' + str(self.attendee.uuid) + '/'
        super().setUp()

    def test_get_returns_specified_attendee_details(self):
        response = self.client.get(self.attendees_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_attendee_data = response.json()

        expected_attendee_data = {
            'uuid': str(self.attendee.uuid),
            'username': self.attendee.user.username,
            'email': self.attendee.user.email,
        }

        self.assertDictEqual(expected_attendee_data, actual_attendee_data)


class AttendeeListViewTestCase(TestCase):
    def setUp(self):
        self.attendees_list_url = '/api/attendees/'
        super().setUp()

    def test_get_returns_all_attendees(self):
        first_attendee = AttendeeFactory()
        second_attendee = AttendeeFactory()

        response = self.client.get(self.attendees_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_data = response.json()
        expected_data = [
            {
                'uuid': str(first_attendee.uuid),
                'username': first_attendee.user.username,
                'email': first_attendee.user.email,
            },
            {
                'uuid': str(second_attendee.uuid),
                'username': second_attendee.user.username,
                'email': second_attendee.user.email,
            }
        ]
        self.assertListEqual(actual_data, expected_data)

    def test_post_create_an_attendee_and_a_user_with_it(self):
        attendee_data = {
            'username': 'JuãoPáulu',
            'email': 'juao.paulu@host.com',
            'password': 'xoriugui',
        }

        response = self.client.post(self.attendees_list_url, data=attendee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_attendee_data = response.json()

        persisted_attendee = Attendee.objects.get(uuid=response_attendee_data['uuid'])

        self.assertEqual(persisted_attendee.user.username, response_attendee_data['username'])
        self.assertEqual(persisted_attendee.user.email, response_attendee_data['email'])
        self.assertTrue(check_password(password=attendee_data['password'], encoded=persisted_attendee.user.password))


class PlayDetailViewTestCase(TestCase):
    def setUp(self):
        self.noisy_play = PlayFactory()
        self.play = PlayFactory()
        self.play_data = {
            'uuid': str(self.play.uuid),
            'name': self.play.name,
            'fee': self.play.fee,
            'price': self.play.price,
            'total_accents': self.play.total_accents,
            'amount_of_available_accents': self.play.amount_of_available_accents,
            'revenue': self.play.revenue,
            'total_fee': self.play.total_fee,
        }

        self.plays_detail_url = '/api/plays/' + str(self.play.uuid) + '/'

        super().setUp()

    def test_get_returns_specified_play_details(self):
        response = self.client.get(self.plays_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertDictEqual(response_data, self.play_data)

    def test_put_updates_specified_play_writable_fields(self):
        updated_play_data = self.play_data.copy()

        # Randomly updates play

        updated_play_data['name'] = self.play_data['name'] + 'S'
        updated_play_data['price'] = self.play_data['price'] + 1.1
        updated_play_data['fee'] = self.play_data['price'] + 0.1
        updated_play_data['total_accents'] = self.play_data['total_accents']

        response = self.client.put(self.plays_detail_url, data=updated_play_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertDictEqual(response_data, updated_play_data)

        persisted_play = Play.objects.get(uuid=updated_play_data['uuid'])

        self.assertEqual(persisted_play.name, updated_play_data['name'])
        self.assertEqual(persisted_play.price, updated_play_data['price'])
        self.assertEqual(persisted_play.fee, updated_play_data['fee'])
        self.assertEqual(persisted_play.total_accents, updated_play_data['total_accents'])

    def test_patch_updates_specified_play_writable_field(self):
        updated_play_data = self.play_data.copy()

        # Randomly updates play

        updated_play_data['price'] = self.play_data['price'] + 1.1

        response = self.client.patch(self.plays_detail_url, data=updated_play_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertDictEqual(response_data, updated_play_data)

        persisted_play = Play.objects.get(uuid=updated_play_data['uuid'])

        self.assertEqual(persisted_play.price, updated_play_data['price'])

    def test_delete_returns_204_and_removes_specified_play_and_its_reservations(self):
        noisy_reservation = ReservationFactory(play=self.noisy_play)
        reservation_1 = ReservationFactory(play=self.play)
        reservation_2 = ReservationFactory(play=self.play)

        response = self.client.delete(self.plays_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertIsNone(Play.objects.filter(uuid=self.play.uuid).first())
        self.assertIsNone(Reservation.objects.filter(uuid=reservation_1.uuid).first())
        self.assertIsNone(Reservation.objects.filter(uuid=reservation_2.uuid).first())

        self.assertIsNotNone(Play.objects.get(uuid=self.noisy_play.uuid))
        self.assertIsNotNone(Reservation.objects.get(uuid=noisy_reservation.uuid))


class PlayListViewTestCase(TestCase):
    def setUp(self):
        self.plays_list_url = '/api/plays/'
        super().setUp()

    def test_get_returns_all_plays(self):
        first_play = PlayFactory()
        second_play = PlayFactory()

        response = self.client.get(self.plays_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_data = response.json()
        expected_data = [
            {
                'uuid': str(first_play.uuid),
                'name': first_play.name,
                'fee': first_play.fee,
                'price': first_play.price,
                'total_accents': first_play.total_accents,
            },
            {
                'uuid': str(second_play.uuid),
                'name': second_play.name,
                'fee': second_play.fee,
                'price': second_play.price,
                'total_accents': second_play.total_accents,
            }
        ]

        self.assertListEqual(actual_data, expected_data)

    def test_post_creates_a_play_with_sent_data(self):
        play_data = {
            'name': 'Play Name',
            'price': 10.,
            'fee': 0.3,
            'total_accents': 5,
        }

        response = self.client.post(self.plays_list_url, data=play_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_play_data = response.json()

        persisted_play = Play.objects.get(uuid=response_play_data['uuid'])

        self.assertEqual(persisted_play.name, response_play_data['name'])
        self.assertEqual(persisted_play.price, response_play_data['price'])
        self.assertEqual(persisted_play.fee, response_play_data['fee'])
        self.assertEqual(persisted_play.total_accents, response_play_data['total_accents'])


class ReservationDetailViewTestCase(TestCase):
    def setUp(self):
        self.noisy_reservation = ReservationFactory()
        self.reservation = ReservationFactory()
        self.reservation_detail_url = '/api/reservations/' + str(self.reservation.uuid) + '/'

    def test_get_returns_specified_reservation_data(self):
        response = self.client.get(self.reservation_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_reservation_data = response.json()
        expected_reservation_data = {
            'uuid': str(self.reservation.uuid),
            'play': str(self.reservation.play.uuid),
            'attendee': str(self.reservation.attendee.uuid),
        }

        self.assertEqual(expected_reservation_data, actual_reservation_data)

    def test_put_or_patch_returns_405_method_not_allowed(self):
        put_response = self.client.put(self.reservation_detail_url, data={})
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        patch_response = self.client.patch(self.reservation_detail_url, data={})
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_returns_204_and_removes_only_specified_reservation_and_keeps_play_and_attendee(self):
        play_uuid = str(self.reservation.play.uuid)
        attendee_uuid = str(self.reservation.attendee.uuid)

        response = self.client.delete(self.reservation_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertIsNotNone(Play.objects.get(uuid=play_uuid))
        self.assertIsNotNone(Attendee.objects.get(uuid=attendee_uuid))

        self.assertIsNotNone(Play.objects.get(uuid=str(self.noisy_reservation.play.uuid)))
        self.assertIsNotNone(Attendee.objects.get(uuid=str(self.noisy_reservation.attendee.uuid)))


class ReservationListViewTestCase(TestCase):
    def setUp(self):
        self.reservations_list_url = '/api/reservations/'
        super().setUp()

    def test_get_returns_all_reservations(self):
        expected_reservations_data = []

        play_1 = PlayFactory()
        play_2 = PlayFactory()

        attendee_for_plays_1_2 = AttendeeFactory()
        play_1_reservation = ReservationFactory(play=play_1, attendee=attendee_for_plays_1_2)
        play_2_reservation = ReservationFactory(play=play_2, attendee=attendee_for_plays_1_2)

        expected_reservations_data += [
            {
                'uuid': str(play_1_reservation.uuid),
                'play': str(play_1.uuid),
                'attendee': str(attendee_for_plays_1_2.uuid),
            },
            {
                'uuid': str(play_2_reservation.uuid),
                'play': str(play_2.uuid),
                'attendee': str(attendee_for_plays_1_2.uuid),
            }
        ]

        attendee_for_play_1 = AttendeeFactory()
        play_1_reservation = ReservationFactory(play=play_1, attendee=attendee_for_play_1)

        expected_reservations_data += [
            {
                'uuid': str(play_1_reservation.uuid),
                'play': str(play_1.uuid),
                'attendee': str(attendee_for_play_1.uuid),
            }
        ]

        attendee_for_play_2 = AttendeeFactory()
        play_2_reservation = ReservationFactory(play=play_2, attendee=attendee_for_play_2)

        expected_reservations_data += [
            {
                'uuid': str(play_2_reservation.uuid),
                'play': str(play_2.uuid),
                'attendee': str(attendee_for_play_2.uuid),
            }
        ]

        play_with_no_reservation = PlayFactory()
        attendee_with_no_reservation = AttendeeFactory()

        response = self.client.get(self.reservations_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_reservations_data = response.json()

        self.assertListEqual(expected_reservations_data, actual_reservations_data)

    def test_post_returns_201_and_creates_attendee_reservation_for_play(self):
        play = PlayFactory()
        attendee = AttendeeFactory()
        reservation_data = {
            'attendee': str(attendee.uuid),
            'play': str(play.uuid),
        }

        response = self.client.post(self.reservations_list_url, data=reservation_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_reservation_response_data = response.json()

        persisted_reservation = Reservation.objects.get(uuid=created_reservation_response_data['uuid'])
        expected_reservation = Reservation(attendee=attendee, play=play)

        self.assertEqual(persisted_reservation.attendee, expected_reservation.attendee)
        self.assertEqual(persisted_reservation.play, expected_reservation.play)

    def test_post_returns_400_when_attendee_attempts_more_than_one_reservation_for_the_same_play(self):
        reservation = ReservationFactory()

        duplicate_reservation_data = {
            'attendee': str(reservation.attendee.uuid),
            'play': str(reservation.play.uuid),
        }

        response = self.client.post(
            self.reservations_list_url, data=duplicate_reservation_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        attendee = Attendee.objects.get(uuid=str(reservation.attendee.uuid))
        expected_attendee_reservations_count = 1
        actual_attendee_reservations_count = attendee.reservations.count()

        self.assertEqual(expected_attendee_reservations_count, actual_attendee_reservations_count)

        play = Play.objects.get(uuid=str(reservation.play.uuid))
        expected_play_reservations_count = 1
        actual_play_reservations_count = play.reservations.count()

        self.assertEqual(expected_play_reservations_count, actual_play_reservations_count)
