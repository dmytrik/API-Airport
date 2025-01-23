from django_filters import rest_framework as filters

from airport.models import (
    Airplane,
    Route,
    Airport,
    AirplaneType
)


class AirplaneFilter(filters.FilterSet):
    """
    Filter class for the Airplane model.

    Allows filtering of airplanes based on their name
    using the 'icontains' lookup expression.
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Airplane
        fields = ("name",)


class RouteFilter(filters.FilterSet):
    """
    Filter class for the Route model.

    Allows filtering of routes based on the source and
    destination airports' closest big city using
    the 'icontains' lookup expression for both fields.
    """

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
    """
    Filter class for the Airport model.

    Allows filtering of airports based on their name or closest big city
    using the 'icontains' lookup expression for both fields.
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    city = filters.CharFilter(field_name="closest_big_city", lookup_expr="icontains")

    class Meta:
        model = Airport
        fields = ("name", "city")


class AirplaneTypeFilter(filters.FilterSet):
    """
    Filter class for the AirplaneType model.

    Allows filtering of airplane types based on their
    name using the 'icontains' lookup expression.
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = AirplaneType
        fields = ("name",)
