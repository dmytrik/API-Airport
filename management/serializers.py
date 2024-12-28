from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from management.models import (
    Ticket,
    Flight,
    Order
)
from airport.serializers import (
    RouteListDetailSerializer,
    CrewSerializer,
    AirplaneListDetailSerializer
)


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
            "purchased_tickets",
        )
        read_only_fields = ("id",)

    def get_purchased_tickets(self, obj):
        tickets = obj.tickets.all()
        serializer = TicketFlightSerializer(tickets, many=True)
        return serializer.data


class FlightListSerializer(AvailableSeatsMixin, serializers.ModelSerializer):

    city_from = serializers.CharField(
        source="route.source.closest_big_city", read_only=True
    )
    city_to = serializers.CharField(
        source="route.destination.closest_big_city", read_only=True
    )
    airplane = serializers.SlugRelatedField(read_only=True, slug_field="name")
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
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
            "crew",
        )
        read_only_fields = fields


class TicketSerializer(serializers.ModelSerializer):

    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        read_only_fields = ("id",)
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["flight", "row", "seat"]
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


class OrderSerializer(serializers.ModelSerializer):

    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")
        read_only_fields = ("id",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            tickets = [
                Ticket(
                    row=ticket.get("row"),
                    seat=ticket.get("seat"),
                    flight=ticket.get("flight"),
                    order=order,
                )
                for ticket in tickets_data
            ]
            for ticket in tickets:
                ticket.full_clean()

            Ticket.objects.bulk_create(tickets)

            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
