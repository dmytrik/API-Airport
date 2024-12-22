from django.core.exceptions import ValidationError
from rest_framework import serializers

from airport.models import Ticket
from .flight_serializers import FlightListSerializer

class TicketSerializer(serializers.ModelSerializer):

    flight = FlightListSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        read_only_fields = ("id",)

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_seat(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data
