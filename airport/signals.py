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
def invalidate_crew_cache(sender, instance, **kwargs):
    """
    Invalidates the cache related to the Crew model after
    a Crew instance is saved or deleted.

    This receiver listens to `post_save` and `post_delete`
    signals for the Crew model.
    It removes any cached data associated with views related to
    Crew by deleting cache patterns
    that match "*crew_view*".
    """
    cache.delete_pattern("*crew_view*")


@receiver([post_save, post_delete], sender=Airport)
def invalidate_airport_cache(sender, instance, **kwargs):
    """
    Invalidates the cache related to the Airport model after
    an Airport instance is saved or deleted.

    This receiver listens to `post_save` and `post_delete`
    signals for the Airport model.
    It removes any cached data associated with views related
    to Airport by deleting cache patterns
    that match "*airport_view*".
    """
    cache.delete_pattern("*airport_view*")


@receiver([post_save, post_delete], sender=Airplane)
def invalidate_airplane_cache(sender, instance, **kwargs):
    """
    Invalidates the cache related to the Airplane model after
    an Airplane instance is saved or deleted.

    This receiver listens to `post_save` and `post_delete`
    signals for the Airplane model.
    It removes any cached data associated with views related
    to Airplane by deleting cache patterns
    that match "*airplane_view*".
    """
    cache.delete_pattern("*airplane_view*")


@receiver([post_save, post_delete], sender=AirplaneType)
def invalidate_airplane_type_cache(sender, instance, **kwargs):
    """
    Invalidates the cache related to the AirplaneType model
    after an AirplaneType instance is saved or deleted.

    This receiver listens to `post_save` and `post_delete`
    signals for the AirplaneType model.
    It removes any cached data associated with views
    related to AirplaneType by deleting cache patterns
    that match "*airplane_type_view*".
    """
    cache.delete_pattern("*airplane_type_view*")


@receiver([post_save, post_delete], sender=Route)
def invalidate_route_cache(sender, instance, **kwargs):
    """
    Invalidates the cache related to the Route model after
    a Route instance is saved or deleted.

    This receiver listens to `post_save` and `post_delete`
    signals for the Route model.
    It removes any cached data associated with views related
    to Route by deleting cache patterns
    that match "*route_view*".
    """
    cache.delete_pattern("*route_view*")
