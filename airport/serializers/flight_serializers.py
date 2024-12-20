from rest_framework import serializers

from airport.models import Flight


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id",)


class FlightTicketAppereanceSerializer(serializers.ModelSerializer):

    from_ = serializers.CharField(source="route.source.name")
    to_ = serializers.CharField(source="route.destination.name")

    class Meta:
        model = Flight
        fields = ("id", "from_", "to_")
        read_only_fields = fields
