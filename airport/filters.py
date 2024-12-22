from django_filters import rest_framework as filters
from airport.models import Airplane, Flight


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

    class Meta:
        model = Flight
        fields = ("city_from", "city_to")
