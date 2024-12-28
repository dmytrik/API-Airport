from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import (
    viewsets,
    mixins,
)
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
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="crew_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="airport_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListDetailSerializer
        return AirplaneSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="airplane_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    queryset = AirplaneType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneTypeFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @method_decorator(cache_page(60 * 5, key_prefix="airplane_type_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source",
        "destination",
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListDetailSerializer
        return RouteSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="route_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
