from rest_framework import routers

from airport.views import (
    AirportViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    RouteViewSet,
    CrewViewSet,
)


app_name = "airport"

router = routers.DefaultRouter()

router.register("airports", AirportViewSet, basename="airports")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("airplane-types", AirplaneTypeViewSet, basename="airplane-types")
router.register("crew", CrewViewSet, basename="crews")
router.register("routers", RouteViewSet, basename="routers")

urlpatterns = router.urls
