from django_filters import rest_framework as filters
from airport.models import (
    Airplane,
    Flight,
    Route,
    Airport,
    AirplaneType
)


class AirplaneFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Airplane
        fields = ("name",)


class FlightFilter(filters.FilterSet):

    city_from = filters.CharFilter(
        field_name="route__source__closest_big_city",
        lookup_expr="icontains"
    )
    city_to = filters.CharFilter(
        field_name="route__destination__closest_big_city",
        lookup_expr="icontains"
    )
    departure_time = filters.DateFilter(
        field_name="departure_time",
        lookup_expr="icontains"
    )

    class Meta:
        model = Flight
        fields = ("city_from", "city_to", "departure_time")


class RouteFilter(filters.FilterSet):

    source = filters.CharFilter(
        field_name="source__closest_big_city",
        lookup_expr="icontains"
    )
    destination = filters.CharFilter(
        field_name="destination__closest_big_city",
        lookup_expr="icontains"
    )

    class Meta:
        model = Route
        fields = ("source", "destination")


class AirportFilter(filters.FilterSet):

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    city = filters.CharFilter(
        field_name="closest_big_city",
        lookup_expr="icontains"
    )

    class Meta:
        model = Airport
        fields = ("name", "city")


class AirplaneTypeFilter(filters.FilterSet):

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = AirplaneType
        fields = ("name",)
