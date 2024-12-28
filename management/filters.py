from django_filters import rest_framework as filters

from management.models import Flight


class FlightFilter(filters.FilterSet):

    city_from = filters.CharFilter(
        field_name="route__source__closest_big_city", lookup_expr="icontains"
    )
    city_to = filters.CharFilter(
        field_name="route__destination__closest_big_city", lookup_expr="icontains"
    )
    departure_time = filters.DateFilter(
        field_name="departure_time", lookup_expr="icontains"
    )

    class Meta:
        model = Flight
        fields = ("city_from", "city_to", "departure_time")
