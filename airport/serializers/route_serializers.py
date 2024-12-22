from rest_framework import serializers

from airport.models import Route
from .airport_serializers import AirportSerializer


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id",)


class RouteListDetailSerializer(RouteSerializer):
    source = AirportSerializer(
        read_only=True
    )
    destination = AirportSerializer(
        read_only=True
    )
