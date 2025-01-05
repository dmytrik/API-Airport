from django.contrib import admin

from management.models import (
    Flight,
    Ticket,
    Order
)


admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Order)
