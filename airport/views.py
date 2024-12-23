from rest_framework import (
    viewsets,
    mixins,
)
from django_filters import rest_framework as filters

from airport.serializers import (
    OrderSerializer,
    TicketSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListDetailSerializer,
    AirplaneSerializer,
    AirplaneListDetailSerializer,
    AirplaneTypeSerializer
)
from airport.models import (
    Order,
    Ticket,
    Flight,
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Route
)
from airport.filters import (
    AirplaneFilter,
    FlightFilter,
    RouteFilter,
    AirportFilter,
    AirplaneTypeFilter
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            "tickets__flight__route__source",
            "tickets__flight__route__destination",
            "tickets__flight__airplane",
            "tickets__flight__crew"
        )
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.select_related(
            "flight__route__source",
            "flight__route__destination",
            "flight__airplane",
            "order"
        ).prefetch_related("flight__crew")
        return queryset.filter(order__user=self.request.user)


class FlightViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        return Flight.objects.select_related(
            "route__source",
            "route__destination",
            "airplane__airplane_type"
        ).prefetch_related(
            "crew",
        )

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListDetailSerializer
        return AirplaneSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneTypeFilter


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source",
        "destination",
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListDetailSerializer
        return RouteSerializer
