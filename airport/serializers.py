from rest_framework import serializers

from airport.models import (
    Airport,
    Order,
    Ticket,
    Flight,
    Crew,
    Airplane,
    AirplaneType,
    Route
)

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")
        read_only_fields = ("id",)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        read_only_fields = ("id",)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id",)


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id",)


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "full_name")
        read_only_fields = ("id",)


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ("id", "name", "capacity", "airplane_type")
        read_only_fields = ("id",)


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")
        read_only_fields = ("id",)
