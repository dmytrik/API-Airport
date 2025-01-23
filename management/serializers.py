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
    AirplaneListDetailSerializer,
)


class AvailableSeatsMixin:
    """
    Mixin class to provide a method for calculating
    the number of available seats on a flight.

    Methods:
        get_count_available_seats(obj): Returns the
        number of available seats on a flight by subtracting
        the count of booked tickets from the airplane's capacity.
    """

    def get_count_available_seats(self, obj):
        """
        Returns the number of available seats on
        a flight by calculating the remaining seats.

        Args:
            obj (Flight): The flight object to calculate
            available seats for.

        Returns:
            int: The number of available seats on the flight.
        """

        tickets_count = obj.tickets.count()
        capacity = obj.airplane.capacity

        return capacity - tickets_count


class TicketFlightSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model used in flight details.

    Fields:
        id (int): The unique identifier of the ticket.
        row (int): The row number of the seat on the airplane.
        seat (int): The seat number within the row.

    Meta:
        model: Ticket
        fields: ('id', 'row', 'seat')
        read_only_fields: ('id',)
    """

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat")
        read_only_fields = ("id",)


class FlightSerializer(serializers.ModelSerializer):
    """
    Serializer for the Flight model used in basic
    flight data representation.

    Fields:
        id (int): The unique identifier of the flight.
        route (Route): The route of the flight, linking
        source and destination airports.
        airplane (Airplane): The airplane used for the flight.
        departure_time (datetime): The departure time of the flight.
        arrival_time (datetime): The arrival time of the flight.
        crew (list): List of crew members assigned to the flight.

    Meta:
        model: Flight
        fields: ('id', 'route', 'airplane', 'departure_time',
        'arrival_time', 'crew')
        read_only_fields: ('id',)
    """

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew"
        )
        read_only_fields = ("id",)


class FlightDetailSerializer(AvailableSeatsMixin, serializers.ModelSerializer):
    """
    Serializer for detailed flight information,
    including available seats and purchased tickets.

    Fields:
        id (int): The unique identifier of the flight.
        route (RouteListDetailSerializer): Detailed route
        information, including source and destination airports.
        airplane (AirplaneListDetailSerializer):
        Detailed airplane information.
        count_available_seats (int): The number of available
        seats on the flight.
        departure_time (datetime): The departure time
        of the flight.
        arrival_time (datetime): The arrival time of the flight.
        crew (CrewSerializer): List of crew members
        on the flight.
        purchased_tickets (list): A list of purchased
        tickets for the flight.

    Methods:
        get_purchased_tickets(obj): Returns a list of tickets
        purchased for the flight.
        get_count_available_seats(obj): Returns the number
        of available seats on the flight.
    """

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
        """
        Returns a list of purchased tickets for the given flight.

        Args:
            obj (Flight): The flight object.

        Returns:
            list: A list of serialized ticket data.
        """

        tickets = obj.tickets.all()
        serializer = TicketFlightSerializer(tickets, many=True)
        return serializer.data


class FlightListSerializer(AvailableSeatsMixin, serializers.ModelSerializer):
    """
    Serializer for listing flights with basic flight
    information and available seats.

    Fields:
        id (int): The unique identifier of the flight.
        city_from (str): The source city of the flight route.
        city_to (str): The destination city of the flight route.
        airplane (str): The name of the airplane used for the flight.
        departure_time (datetime): The departure time of the flight.
        arrival_time (datetime): The arrival time of the flight.
        count_available_seats (int): The number of available seats on the flight.
        crew (list): List of crew members on the flight.

    Methods:
        get_count_available_seats(obj): Returns the number
        of available seats on the flight.
    """

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
    """
    Serializer for the Ticket model, used to create and manage ticket data.

    Fields:
        id (int): The unique identifier of the ticket.
        row (int): The row number of the seat on the airplane.
        seat (int): The seat number within the row.
        flight (int): The primary key of the associated flight for the ticket.

    Meta:
        model: Ticket
        fields: ('id', 'row', 'seat', 'flight')
        read_only_fields: ('id',)
        validators: Ensures a unique combination of flight, row, and seat.

    Methods:
        validate(attrs): Validates the seat information for the ticket.
    """

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
        """
        Validates the ticket data, ensuring that the seat is
        within the allowable range.

        Args:
            attrs (dict): The attributes of the ticket.

        Returns:
            dict: The validated data.

        Raises:
            ValidationError: If the seat or row is not within
            the allowed range.
        """
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
    """
    Serializer for the Order model, used to create and manage
    orders for tickets.

    Fields:
        id (int): The unique identifier of the order.
        created_at (datetime): The creation timestamp of the order.
        tickets (list): A list of tickets associated with the order.

    Methods:
        create(validated_data): Creates an order and associated
        tickets in a transaction.
    """

    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """
        Creates an order and its associated tickets in
        a transaction, ensuring atomicity.

        Args:
            validated_data (dict): The validated data
            for creating the order.

        Returns:
            Order: The created order object.
        """

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

    def update(self, instance, validated_data):
        """
        Update the Order instance with the provided validated
        data, including handling updates to associated tickets.

        This method first updates the main fields of the Order
        instance with the provided validated data.
        If the validated data contains tickets, the existing
        tickets associated with the Order are deleted and replaced
        with the new tickets. This ensures that only the
        tickets provided in the update request are kept.

        Parameters:
        - instance (Order): The Order instance to be updated.
        - validated_data (dict): A dictionary of validated data,
         which can contain updates for the Order fields
          and optionally the associated tickets.

        Returns:
        - Order: The updated Order instance.

        If tickets data is provided, the existing tickets
        associated with the Order are deleted and replaced
        with the new tickets
        passed in the validated data. Otherwise, only the
        other fields of the Order instance are updated.
        """

        tickets_data = validated_data.pop("tickets", None)
        instance = super().update(instance, validated_data)

        if tickets_data is not None:
            instance.tickets.all().delete()

            tickets = [
                Ticket(
                    row=ticket.get("row"),
                    seat=ticket.get("seat"),
                    flight=ticket.get("flight"),
                    order=instance,
                )
                for ticket in tickets_data
            ]

            Ticket.objects.bulk_create(tickets)

        return instance


class OrderListSerializer(OrderSerializer):
    """
    Serializer for listing orders, including detailed
    ticket information.

    Fields:
        id (int): The unique identifier of the order.
        created_at (datetime): The creation timestamp
        of the order.
        tickets (list): A list of tickets associated
        with the order.
    """

    tickets = TicketSerializer(many=True, read_only=True)
