from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer
from rest_framework.fields import CharField, EmailField, UUIDField

from .models import Attendee, Play, Reservation


class AttendeeSerializer(Serializer):
    uuid = UUIDField(read_only=True)
    username = CharField(source='user.username')
    password = CharField(source='user.password', write_only=True)
    email = EmailField(source='user.email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'])
        attendee = Attendee.objects.create(user=user)
        return attendee


class PlaySerializer(ModelSerializer):
    class Meta:
        model = Play
        fields = ('uuid', 'name', 'fee', 'price', 'total_accents')
        read_only_fields = ('uuid', )


class PlayFinancialDetailSerializer(ModelSerializer):
    class Meta:
        model = Play
        fields = ('uuid', 'name', 'fee', 'price', 'total_accents',
                  'amount_of_available_accents', 'revenue', 'total_fee')
        read_only_fields = ('uuid', 'amount_of_available_accents', 'revenue', 'total_fee')


class ReservationSerializer(ModelSerializer):
    attendee = PrimaryKeyRelatedField(queryset=Attendee.objects.all())
    play = PrimaryKeyRelatedField(queryset=Play.objects.all())

    class Meta:
        model = Reservation
        fields = ('uuid', 'attendee', 'play')
        read_only_fields = ('uuid', )
