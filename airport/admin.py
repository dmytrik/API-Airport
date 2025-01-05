from django.contrib import admin

from airport.models import (
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Route,
)

admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Route)
