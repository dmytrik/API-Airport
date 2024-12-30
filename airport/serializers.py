from rest_framework import serializers

from airport.models import (
    Route,
    Crew,
    Airport,
    Airplane,
    AirplaneType
)


class AirportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Airport model.

    Fields:
        - id: Unique identifier for the airport (read-only).
        - name: Name of the airport.
        - closest_big_city: The closest large city to the airport.

    Read-only Fields:
        - id
    """

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")
        read_only_fields = ("id",)


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.

    Fields:
        - id: Unique identifier for the route (read-only).
        - source: The source airport of the route.
        - destination: The destination airport of the route.
        - distance: The distance of the route.

    Read-only Fields:
        - id
    """

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id",)


class RouteListDetailSerializer(RouteSerializer):
    """
    Serializer for the Route model with detailed source
    and destination airport information.

    Inherits from RouteSerializer and adds detailed airport
    information by using the AirportSerializer.

    Fields:
        - source: Detailed source airport information
        (using AirportSerializer).
        - destination: Detailed destination airport information
        (using AirportSerializer).
    """

    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crew model.

    Fields:
        - id: Unique identifier for the crew member (read-only).
        - first_name: The first name of the crew member.
        - last_name: The last name of the crew member.
        - full_name: The full name of the crew member (first name + last name).

    Read-only Fields:
        - id
    """

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")
        read_only_fields = ("id",)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the AirplaneType model.

    Fields:
        - id: Unique identifier for the airplane type (read-only).
        - name: The name of the airplane type.

    Read-only Fields:
        - id
    """

    class Meta:
        model = AirplaneType
        fields = ("id", "name")
        read_only_fields = ("id",)


class AirplaneSerializer(serializers.ModelSerializer):
    """
    Serializer for the Airplane model.

    Fields:
        - id: Unique identifier for the airplane (read-only).
        - name: The name of the airplane.
        - rows: The number of rows in the airplane.
        - seats_in_row: The number of seats in each row.
        - capacity: The total seating capacity of the airplane (calculated).
        - airplane_type: The type of the airplane.

    Read-only Fields:
        - id
    """

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type"
        )
        read_only_fields = ("id",)


class AirplaneListDetailSerializer(AirplaneSerializer):
    """
    Serializer for the Airplane model with detailed
    airplane type information.

    Inherits from AirplaneSerializer and adds the
    airplane type's name as a field.

    Fields:
        - airplane_type: The name of the airplane
        type (read-only).
    """

    airplane_type = serializers.CharField(
        source="airplane_type.name",
        read_only=True
    )
