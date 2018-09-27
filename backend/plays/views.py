from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
)

from .models import Attendee, Play, Reservation
from .serializers import AttendeeSerializer, PlaySerializer, PlayFinancialDetailSerializer, ReservationSerializer


class AttendeeListView(ListCreateAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()


class AttendeeDetailView(RetrieveAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()


class PlayListView(ListCreateAPIView):
    serializer_class = PlaySerializer
    queryset = Play.objects.all()


class PlayDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PlayFinancialDetailSerializer
    queryset = Play.objects.all()


class ReservationListView(ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationDetailView(RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
