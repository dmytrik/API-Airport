import uuid

from django.db import models


class UUIDBaseModel(models.Model):
    """
    Abstract base model that provides a UUID
    primary key for subclasses.

    This model serves as a base class for
    other models, automatically generating
    a unique UUID (`id`) for each instance.
    The `id` field is set as the primary key
    and cannot be edited.

    Attributes:
        id (UUIDField): A universally unique
        identifier (UUID) for each model instance.

    Meta:
        abstract (bool): Indicates that this model
        is abstract, and it will not be created
        as a database table. It is intended
        to be inherited by other models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
