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
    FlightListSerializer,
)
from management.filters import FlightFilter
from management.models import (
    Order,
    Flight,
    Ticket
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Order` instances.

    This viewset allows authenticated users to list, retrieve, create, update, or delete
    orders, but only their own orders can be accessed or modified. It uses the `OrderSerializer`
    for creating and updating orders and the `OrderListSerializer` for listing and retrieving orders.
    The viewset ensures that the user can only interact with their own orders.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access their orders.

    Caching:
        - `cache_page`: Caches the response for 5 minutes to improve performance for orders views.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filters orders to return only those that belong to the authenticated user.

        The queryset is prefetched with related models (`tickets`, `flights`, `routes`, etc.)
        to optimize database queries.
        """

        queryset = Order.objects.prefetch_related(
            "tickets__flight__route__source",
            "tickets__flight__route__destination",
            "tickets__flight__airplane",
            "tickets__flight__crew",
        )
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action being performed.

        - "list" or "retrieve" action: `OrderListSerializer`
        - Any other action: `OrderSerializer`
        """

        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """
        Overrides the `perform_create` method to automatically associate the authenticated user
        with the order being created.
        """

        serializer.save(user=self.request.user)

    @method_decorator(cache_page(60 * 5, key_prefix="order_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Applies caching to the viewset actions, caching the response for 5 minutes
        using a key prefix of `order_view`.
        """

        return super().dispatch(request, *args, **kwargs)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing `Ticket` instances.

    This viewset allows authenticated users to view tickets associated with their orders.
    It uses the `TicketSerializer` for presenting the ticket data.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access tickets related to their orders.

    Caching:
        - `cache_page`: Caches the response for 5 minutes to improve performance for ticket views.
    """

    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filters tickets to return only those associated with orders that belong to the authenticated user.

        The queryset is optimized with `select_related` and `prefetch_related` for related models
        (`flights`, `routes`, `airplanes`, etc.).
        """

        queryset = Ticket.objects.select_related(
            "flight__route__source",
            "flight__route__destination",
            "flight__airplane",
            "order",
        ).prefetch_related("flight__crew")
        return queryset.filter(order__user=self.request.user)

    @method_decorator(cache_page(60 * 5, key_prefix="ticket_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Applies caching to the viewset actions, caching the response for 5 minutes
        using a key prefix of `ticket_view`.
        """

        return super().dispatch(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Flight` instances.

    This viewset allows both administrators and authenticated users (with restricted permissions)
    to manage flights, including listing, retrieving, and modifying flight details. It uses
    the `FlightSerializer`, `FlightListSerializer`, and `FlightDetailSerializer` for serializing
    flight data depending on the action being performed.

    Permissions:
        - `IsAdminOrIfAuthenticatedReadOnly`: Grants full access to admins, while authenticated
          users have read-only access.

    Caching:
        - `cache_page`: Caches the response for 5 minutes to improve performance for flight views.
    """

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = Flight.objects.select_related(
        "route__source", "route__destination", "airplane__airplane_type"
    ).prefetch_related("crew", "tickets")

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action being performed.

        - "list" action: `FlightListSerializer`
        - "retrieve" action: `FlightDetailSerializer`
        - Any other action: `FlightSerializer`
        """

        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="flight_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Applies caching to the viewset actions, caching the response for 5 minutes
        using a key prefix of `flight_view`.
        """

        return super().dispatch(request, *args, **kwargs)
