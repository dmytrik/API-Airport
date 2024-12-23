from rest_framework import serializers

from airport.models import (
    Flight,
    Ticket
)
from .route_serializers import RouteListDetailSerializer
from .crew_serializers import CrewSerializer
from .airplane_serializers import AirplaneListDetailSerializer


class AvailableSeatsMixin:

    def get_count_available_seats(self, obj):
        tickets_count = obj.tickets.count()
        capacity = obj.airplane.capacity

        return capacity - tickets_count


class TicketFlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat")
        read_only_fields = ("id",)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id",)


class FlightDetailSerializer(AvailableSeatsMixin, serializers.ModelSerializer):
    route = RouteListDetailSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    airplane = AirplaneListDetailSerializer(read_only=True)
    purchased_tickets = serializers.SerializerMethodField(read_only=True)
    count_available_seats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "count_available_seats",
            "departure_time",
            "arrival_time",
            "crew",
            "purchased_tickets"
        )
        read_only_fields = ("id",)

    def get_purchased_tickets(self, obj):
        tickets = obj.tickets.all()
        serializer = TicketFlightSerializer(tickets, many=True)
        return serializer.data


class FlightListSerializer(AvailableSeatsMixin, serializers.ModelSerializer):

    city_from = serializers.CharField(
        source="route.source.closest_big_city",
        read_only=True
    )
    city_to = serializers.CharField(
        source="route.destination.closest_big_city",
        read_only=True
    )
    airplane = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    count_available_seats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "city_from",
            "city_to",
            "airplane",
            "departure_time",
            "arrival_time",
            "count_available_seats",
            "crew"
        )
        read_only_fields = fields
