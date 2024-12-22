from rest_framework import serializers

from airport.models import Flight
from .route_serializers import RouteSerializer
from .crew_serializers import CrewSerializer
from .airplane_serializers import AirplaneListDetailSerializer


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id",)


class FlightDetailSerializer(FlightSerializer):
    route = RouteSerializer()
    crew = CrewSerializer(many=True)
    airplane = AirplaneListDetailSerializer()


class FlightListSerializer(serializers.ModelSerializer):

    city_from = serializers.CharField(source="route.source.closest_big_city")
    city_to = serializers.CharField(source="route.destination.closest_big_city")
    airplane = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )

    class Meta:
        model = Flight
        fields = ("id", "city_from", "city_to", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = fields
