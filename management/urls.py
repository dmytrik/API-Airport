from django.urls import path, include
from rest_framework import routers

from management.views import (
    OrderViewSet,
    TicketViewSet,
    FlightViewSet
)


app_name = "management"

router = routers.DefaultRouter()

router.register("orders", OrderViewSet, basename="orders")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("flights", FlightViewSet, basename="flights")

urlpatterns = [path("", include(router.urls))]
