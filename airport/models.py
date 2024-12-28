from django.db import models
from django.db.models import (
    CheckConstraint,
    Q,
    F
)

from base.models import UUIDBaseModel


class Route(UUIDBaseModel):
    source = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                condition=~Q(source=F("destination")),
                name="check_source_not_equal_destination",
            )
        ]

    def __str__(self):
        return f"From {self.source.name} to {self.destination.name}"


class Airport(UUIDBaseModel):
    name = models.CharField(max_length=63, unique=True)
    closest_big_city = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Crew(UUIDBaseModel):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Airplane(UUIDBaseModel):
    name = models.CharField(max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType", on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}, type: {self.airplane_type.name}"


class AirplaneType(UUIDBaseModel):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name
