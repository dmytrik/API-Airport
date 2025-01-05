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


@receiver([post_save, post_delete])
def invalidate_cache(sender, instance, **kwargs):
    """
    Invalidate specific cache patterns upon model changes.

    This function is triggered by `post_save` and `post_delete` signals for specific models.
    It clears cache entries matching predefined patterns to ensure cache consistency
    when data is modified.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Model instance): The instance of the model that was saved or deleted.
        **kwargs: Additional keyword arguments provided by the signal.
    """
    pattern_dict = {
        Crew: "*crew_view*",
        Airport: "*airport_view*",
        Airplane: "*airplane_view*",
        AirplaneType: "*airplane_type_view*",
        Route: "*route_view*"
    }
    if sender in pattern_dict:
        cache.delete_pattern(pattern_dict[sender])
