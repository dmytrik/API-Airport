from django.db import models
from django.db.models import (
    CheckConstraint,
    Q,
    F
)

from base.models import UUIDBaseModel


class Route(UUIDBaseModel):
    """
    Model representing a route between two airports.

    Attributes:
        source (ForeignKey):
            The source airport of the route.
        destination (ForeignKey):
            The destination airport of the route.
        distance (PositiveIntegerField):
            The distance of the route in kilometers or miles.

    Constraints:
        Ensures that the source airport is not the
        same as the destination airport.
    """

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
    """
    Model representing an airport.

    Attributes:
        name (CharField): The name of the airport (unique).
        closest_big_city (CharField):
        The closest large city to the airport.
    """

    name = models.CharField(max_length=63, unique=True)
    closest_big_city = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Crew(UUIDBaseModel):
    """
    Model representing a crew member.

    Attributes:
        first_name (CharField): The first name of the crew member.
        last_name (CharField): The last name of the crew member.

    Properties:
        full_name (str): The full name of
        the crew member (first name + last name).
    """

    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Airplane(UUIDBaseModel):
    """
    Model representing an airplane.

    Attributes:
        name (CharField): The name of the airplane.
        rows (PositiveIntegerField): The number of rows in the airplane.
        seats_in_row (PositiveIntegerField): The number of seats in each row.
        airplane_type (ForeignKey): The type of the airplane.

    Properties:
        capacity (int): The total seating capacity of the airplane (rows * seats per row).
    """

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
    """
    Model representing an airplane type.

    Attributes:
        name (CharField): The name of the airplane type.
    """

    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name
