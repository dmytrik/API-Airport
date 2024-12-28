from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache

from management.models import Flight, Ticket, Order


@receiver([post_save, post_delete], sender=Flight)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*flight_view*")


@receiver([post_save, post_delete], sender=Ticket)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*ticket_view*")


@receiver([post_save, post_delete], sender=Order)
def invalidate_flight_cache(sender, instance, **kwargs):
    cache.delete_pattern("*order_view*")
