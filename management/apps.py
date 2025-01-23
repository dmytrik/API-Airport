from django.apps import AppConfig


class ManagementConfig(AppConfig):
    """
    Configuration for the management application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "management"

    def ready(self):
        import management.signals  # noqa
