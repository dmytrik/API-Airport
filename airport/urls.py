from django.urls import path, include
from rest_framework import routers

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

router.register("orders", OrderViewSet, basename="orders")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("flights", FlightViewSet, basename="flights")
router.register("airports", AirportViewSet, basename="airports")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("airplane-types", AirplaneTypeViewSet, basename="airplane-types")
router.register("crew", CrewViewSet, basename="crew")
router.register("routers", RouteViewSet, basename="routers")

urlpatterns = [
    path("", include(router.urls))
]
