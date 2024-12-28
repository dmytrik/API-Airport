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
        self.full_clean()
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{str(self.flight)}, row: {self.row}, seat: {self.seat}"


class Flight(UUIDBaseModel):
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
