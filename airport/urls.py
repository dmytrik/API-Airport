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
    CrewViewSet,
)


app_name = "airport"

router = routers.DefaultRouter()

router.register("orders", OrderViewSet, basename="order")
router.register("tickets", TicketViewSet, basename="ticket")
router.register("flights", FlightViewSet, basename="flight")
router.register("airports", AirportViewSet, basename="airport")
router.register("airplanes", AirplaneViewSet, basename="airplane")
router.register("airplane-types", AirplaneTypeViewSet, basename="airplane-type")
router.register("crew", CrewViewSet, basename="crew")
router.register("routers", RouteViewSet, basename="router")

urlpatterns = [path("", include(router.urls))]
