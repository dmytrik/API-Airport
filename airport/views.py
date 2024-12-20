from rest_framework.viewsets import ModelViewSet

from airport.serializers import (
    OrderSerializer,
    TicketSerializer,
    FlightSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
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


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class FlightViewSet(ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()


class CrewViewSet(ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()


class AirportViewSet(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()


class AirplaneViewSet(ModelViewSet):
    serializer_class = AirplaneSerializer
    queryset = Airplane.objects.all()


class AirplaneTypeViewSet(ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()


class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
