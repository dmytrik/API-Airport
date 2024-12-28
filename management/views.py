from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated


from management.serializers import (
    TicketSerializer,
    OrderSerializer,
    OrderListSerializer,
    FlightSerializer,
    FlightDetailSerializer,
    FlightListSerializer
)
from management.filters import FlightFilter
from management.models import (
    Order,
    Flight,
    Ticket
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            "tickets__flight__route__source",
            "tickets__flight__route__destination",
            "tickets__flight__airplane",
            "tickets__flight__crew",
        )
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(60 * 5, key_prefix="order_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Ticket.objects.select_related(
            "flight__route__source",
            "flight__route__destination",
            "flight__airplane",
            "order",
        ).prefetch_related("flight__crew")
        return queryset.filter(order__user=self.request.user)

    @method_decorator(cache_page(60 * 5, key_prefix="ticket_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = Flight.objects.select_related(
        "route__source", "route__destination", "airplane__airplane_type"
    ).prefetch_related("crew", "tickets")

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="flight_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
