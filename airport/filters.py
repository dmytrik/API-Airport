from django_filters import rest_framework as filters

from airport.models import (
    Airplane,
    Route,
    Airport,
    AirplaneType
)


class AirplaneFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Airplane
        fields = ("name",)


class RouteFilter(filters.FilterSet):

    source = filters.CharFilter(
        field_name="source__closest_big_city", lookup_expr="icontains"
    )
    destination = filters.CharFilter(
        field_name="destination__closest_big_city", lookup_expr="icontains"
    )

    class Meta:
        model = Route
        fields = ("source", "destination")


class AirportFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    city = filters.CharFilter(field_name="closest_big_city", lookup_expr="icontains")

    class Meta:
        model = Airport
        fields = ("name", "city")


class AirplaneTypeFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = AirplaneType
        fields = ("name",)
