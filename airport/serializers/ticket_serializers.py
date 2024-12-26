from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import Ticket, Flight


class TicketSerializer(serializers.ModelSerializer):

    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        read_only_fields = ("id",)
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["movie_session", "row", "seat"]
            )
        ]

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_seat(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane.rows,
            attrs["flight"].airplane.seats_in_row,
            serializers.ValidationError,
        )
        return data
