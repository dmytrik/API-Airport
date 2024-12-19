from django.contrib import admin

from airport.models import (
    Order,
    Ticket,
    Flight,
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Route,
)

admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Flight)
admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Route)
