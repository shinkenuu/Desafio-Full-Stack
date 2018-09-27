from django.urls import path

from .views import (
    AttendeeDetailView, AttendeeListView, PlayDetailView, PlayListView, ReservationDetailView, ReservationListView
)


urlpatterns = [
    path('attendees/', AttendeeListView.as_view(),
         name='user-list'),

    path('attendees/<uuid:pk>/', AttendeeDetailView.as_view(),
         name='user-detail'),

    path('plays/', PlayListView.as_view(),
         name='play-list'),

    path('plays/<uuid:pk>/', PlayDetailView.as_view(),
         name='play-detail'),

    path('reservations/', ReservationListView.as_view(),
         name='reservation-list'),

    path('reservations/<uuid:pk>/', ReservationDetailView.as_view(),
         name='reservation-detail'),
]
