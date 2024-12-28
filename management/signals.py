from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    post_delete
)
from django.core.cache import cache

from management.models import (
    Flight,
    Ticket,
    Order
)


@receiver([post_save, post_delete], sender=Flight)
def invalidate_flight_cache(sender, instance, **kwargs):
    """
    Signal receiver that invalidates the cache for flight views when a Flight instance
    is created, updated, or deleted.

    This receiver listens for `post_save` and `post_delete` signals on the `Flight` model.
    Whenever a Flight instance is saved or deleted, it will clear the cache for all
    flight views by deleting cache patterns that match `*flight_view*`.

    Args:
        sender (Model): The model class that triggered the signal (in this case, `Flight`).
        instance (Flight): The instance of the `Flight` model that was saved or deleted.
        **kwargs: Additional keyword arguments passed by the signal dispatcher.
    """

    cache.delete_pattern("*flight_view*")


@receiver([post_save, post_delete], sender=Ticket)
def invalidate_ticket_cache(sender, instance, **kwargs):
    """
    Signal receiver that invalidates the cache for ticket views when a Ticket instance
    is created, updated, or deleted.

    This receiver listens for `post_save` and `post_delete` signals on the `Ticket` model.
    Whenever a Ticket instance is saved or deleted, it will clear the cache for all
    ticket views by deleting cache patterns that match `*ticket_view*`.

    Args:
        sender (Model): The model class that triggered the signal (in this case, `Ticket`).
        instance (Ticket): The instance of the `Ticket` model that was saved or deleted.
        **kwargs: Additional keyword arguments passed by the signal dispatcher.
    """

    cache.delete_pattern("*ticket_view*")


@receiver([post_save, post_delete], sender=Order)
def invalidate_order_cache(sender, instance, **kwargs):
    """
    Signal receiver that invalidates the cache for order views when an Order instance
    is created, updated, or deleted.

    This receiver listens for `post_save` and `post_delete` signals on the `Order` model.
    Whenever an Order instance is saved or deleted, it will clear the cache for all
    order views by deleting cache patterns that match `*order_view*`.

    Args:
        sender (Model): The model class that triggered the signal (in this case, `Order`).
        instance (Order): The instance of the `Order` model that was saved or deleted.
        **kwargs: Additional keyword arguments passed by the signal dispatcher.
    """

    cache.delete_pattern("*order_view*")
