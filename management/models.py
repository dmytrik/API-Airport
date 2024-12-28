from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

from base.models import UUIDBaseModel
from airport.models import (
    Airplane,
    Crew,
    Route
)


class Order(UUIDBaseModel):
    """
    Represents an order placed by a user for booking flight tickets.

    Attributes:
        created_at (datetime): The timestamp when the order was created.
        user (ForeignKey): A reference to the user who placed the order.

    Methods:
        __str__(): Returns a string representation of the order using the `created_at` timestamp.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(UUIDBaseModel):
    """
    Represents a ticket for a specific flight. A ticket is associated with a row and seat on an airplane
    and can be linked to an order.

    Attributes:
        row (PositiveIntegerField): The row number on the airplane.
        seat (PositiveIntegerField): The seat number in the row.
        flight (ForeignKey): A reference to the flight for which the ticket was issued.
        order (ForeignKey): A reference to the order associated with the ticket (optional).

    Methods:
        validate_seat(row, seat, num_rows, num_seats, error): Validates if the row and seat numbers are within
                                                          the available range.
        clean(): Validates the seat before saving the ticket.
        save(): Saves the ticket after cleaning and validation.
        __str__(): Returns a string representation of the ticket, including flight details, row, and seat.

    Meta:
        UniqueConstraint: Ensures the combination of row, seat, and flight is unique.
    """

    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        "Flight", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets", null=True, blank=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "flight"], name="unique_ticket"),
        ]

    @staticmethod
    def validate_seat(
        row: int, seat: int, num_rows: int, num_seats: int, error: callable
    ) -> None:
        """
        Validates if the given row and seat are within the valid range for the flight's airplane.

        Args:
            row (int): The row number.
            seat (int): The seat number.
            num_rows (int): The total number of rows available in the airplane.
            num_seats (int): The total number of seats available in each row.
            error (callable): A callable function to raise the error with appropriate messages.
        """

        if not (1 <= row <= num_rows):
            raise error(
                {
                    "row": [
                        f"row number must be in available range: (1, rows): "
                        f"(1, {num_rows})"
                    ]
                }
            )
        if not (1 <= seat <= num_seats):
            raise error(
                {
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): "
                        f"(1, {num_seats})"
                    ]
                }
            )

    def clean(self) -> None:
        """
        Validates the seat before saving the ticket. Ensures the row and seat are within valid ranges.
        """
        self.validate_seat(
            row=self.row,
            seat=self.seat,
            num_rows=self.flight.airplane.rows,
            num_seats=self.flight.airplane.seats_in_row,
            error=ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """
        Saves the ticket after cleaning and validating its data.
        """
        self.full_clean()
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{str(self.flight)}, row: {self.row}, seat: {self.seat}"


class Flight(UUIDBaseModel):
    """
    Represents a flight that connects a route and an airplane, including flight timings and crew assignments.

    Attributes:
        route (ForeignKey): A reference to the route for the flight.
        airplane (ForeignKey): A reference to the airplane used for the flight.
        departure_time (DateTimeField): The departure date and time of the flight.
        arrival_time (DateTimeField): The arrival date and time of the flight.
        crew (ManyToManyField): A many-to-many relationship with crew members assigned to the flight.

    Methods:
        __str__(): Returns a string representation of the flight, including route details and timing information.

    Meta:
        ordering: Orders flights by `departure_time` in descending order.
    """

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return (
            f"{str(self.route)}, departure time: {self.departure_time}"
            f"arrival time: {self.arrival_time}"
        )
