from django.apps import AppConfig


class AirportConfig(AppConfig):
    """
    Configuration for the airport application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "airport"

    def ready(self):
        import airport.signals  # noqa
