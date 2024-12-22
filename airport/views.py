from rest_framework.viewsets import ModelViewSet

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


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(

    ModelViewSet
):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user)


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class CrewViewSet(ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()


class AirportViewSet(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListDetailSerializer
        return AirplaneSerializer


class AirplaneTypeViewSet(ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListDetailSerializer
        return RouteSerializer
