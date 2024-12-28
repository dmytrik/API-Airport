from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache

from airport.models import (
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Route,
)





@receiver([post_save, post_delete], sender=Crew)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*crew_view*")


@receiver([post_save, post_delete], sender=Airport)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airport_view*")


@receiver([post_save, post_delete], sender=Airplane)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airplane_view*")


@receiver([post_save, post_delete], sender=AirplaneType)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*airplane_type_view*")


@receiver([post_save, post_delete], sender=Route)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*route_view*")



