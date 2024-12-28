from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters

from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListDetailSerializer,
    AirplaneSerializer,
    AirplaneListDetailSerializer,
    AirplaneTypeSerializer,
)
from airport.models import (
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Route,
)
from airport.filters import (
    AirplaneFilter,
    RouteFilter,
    AirportFilter,
    AirplaneTypeFilter,
)


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for handling the Crew model, providing the ability to create and list crew members.

    This ViewSet allows authenticated users to list crew members and admins to create new crew members.
    It also implements caching for the crew view responses for 5 minutes.

    Attributes:
        serializer_class (CrewSerializer): The serializer used to convert Crew instances to and from JSON.
        queryset (QuerySet): A QuerySet used to retrieve all Crew instances.
        permission_classes (tuple): A tuple of permission classes that determine the access control.

    Methods:
        dispatch: Decorates the dispatch method to cache responses for 5 minutes.
    """

    serializer_class = CrewSerializer
    queryset = Crew.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="crew_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied for the crew view.

        The response is cached for 5 minutes using the key prefix 'crew_view'.
        """

        return super().dispatch(request, *args, **kwargs)


class AirportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling the Airport model, allowing for CRUD operations on airports.

    This ViewSet provides full CRUD functionality for the Airport model and filters for searching airports.
    It also implements caching for airport view responses for 5 minutes.

    Attributes:
        serializer_class (AirportSerializer): The serializer used to convert Airport instances to and from JSON.
        queryset (QuerySet): A QuerySet used to retrieve all Airport instances.
        filter_backends (tuple): A tuple of filter backends to apply to the queryset.
        filterset_class (AirportFilter): A filter class used to filter airports by specific criteria.
        permission_classes (tuple): A tuple of permission classes that determine the access control.

    Methods:
        dispatch: Decorates the dispatch method to cache responses for 5 minutes.
    """

    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="airport_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied for the airport view.

        The response is cached for 5 minutes using the key prefix 'airport_view'.
        """

        return super().dispatch(request, *args, **kwargs)


class AirplaneViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling the Airplane model, providing CRUD operations for airplanes.

    This ViewSet supports both listing and retrieving airplane instances and provides functionality
    for applying filters based on airplane attributes. The responses are cached for 5 minutes.

    Attributes:
        queryset (QuerySet): A QuerySet used to retrieve all Airplane instances, with airplane type information.
        filter_backends (tuple): A tuple of filter backends to apply to the queryset.
        filterset_class (AirplaneFilter): A filter class used to filter airplanes by specific criteria.
        permission_classes (tuple): A tuple of permission classes that determine the access control.

    Methods:
        get_serializer_class: Returns the appropriate serializer based on the action (list/retrieve or create).
        dispatch: Decorates the dispatch method to cache responses for 5 minutes.
    """

    queryset = Airplane.objects.select_related("airplane_type")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer based on the action.

        If the action is "list" or "retrieve", the AirplaneListDetailSerializer is used.
        For other actions, the AirplaneSerializer is used.
        """

        if self.action in ("list", "retrieve"):
            return AirplaneListDetailSerializer
        return AirplaneSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="airplane_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied for the airplane view.

        The response is cached for 5 minutes using the key prefix 'airplane_view'.
        """

        return super().dispatch(request, *args, **kwargs)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling the AirplaneType model, allowing CRUD operations for airplane types.

    This ViewSet supports CRUD operations for airplane types and implements caching for responses for 5 minutes.

    Attributes:
        serializer_class (AirplaneTypeSerializer): The serializer used to convert AirplaneType instances to and from JSON.
        queryset (QuerySet): A QuerySet used to retrieve all AirplaneType instances.
        filter_backends (tuple): A tuple of filter backends to apply to the queryset.
        filterset_class (AirplaneTypeFilter): A filter class used to filter airplane types by specific criteria.
        permission_classes (tuple): A tuple of permission classes that determine the access control.

    Methods:
        dispatch: Decorates the dispatch method to cache responses for 5 minutes.
    """

    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneTypeFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="airplane_type_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied for the airplane type view.

        The response is cached for 5 minutes using the key prefix 'airplane_type_view'.
        """

        return super().dispatch(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling the Route model, allowing CRUD operations for flight routes.

    This ViewSet supports CRUD operations for routes between airports, with filtering functionality.
    It also implements caching for route view responses for 5 minutes.

    Attributes:
        queryset (QuerySet): A QuerySet used to retrieve all Route instances, with source and destination airports.
        filter_backends (tuple): A tuple of filter backends to apply to the queryset.
        filterset_class (RouteFilter): A filter class used to filter routes by specific criteria.
        permission_classes (tuple): A tuple of permission classes that determine the access control.

    Methods:
        get_serializer_class: Returns the appropriate serializer based on the action (list/retrieve or create).
        dispatch: Decorates the dispatch method to cache responses for 5 minutes.
    """

    queryset = Route.objects.select_related(
        "source",
        "destination",
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer based on the action.

        If the action is "list" or "retrieve", the RouteListDetailSerializer is used.
        For other actions, the RouteSerializer is used.
        """

        if self.action in ("list", "retrieve"):
            return RouteListDetailSerializer
        return RouteSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="route_view"))
    def dispatch(self, request, *args, **kwargs):
        """
        Method to dispatch the request, with caching applied for the route view.

        The response is cached for 5 minutes using the key prefix 'route_view'.
        """

        return super().dispatch(request, *args, **kwargs)
