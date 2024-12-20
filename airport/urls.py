from django.urls import path, include
from rest_framework import routers

from airport.models import Airplane
from airport.views import (
    OrderViewSet,
    TicketViewSet,
    FlightViewSet,
    AirportViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    RouteViewSet,
    CrewViewSet
)


app_name = "airport"

router = routers.DefaultRouter()

router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)
router.register("flights", FlightViewSet)
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("crew", CrewViewSet)
router.register("routers", RouteViewSet)

urlpatterns = [
    path("", include(router.urls))
]
