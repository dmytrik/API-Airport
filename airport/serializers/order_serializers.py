from rest_framework import serializers
from django.db import transaction

from airport.models import Order, Ticket
from .ticket_serializers import TicketSerializer


class OrderSerializer(serializers.ModelSerializer):

    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")
        read_only_fields = ("id",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            tickets = [
                Ticket(
                    row=ticket.get("row"),
                    seat=ticket.get("seat"),
                    flight=ticket.get("flight"),
                    order=order,
                )
                for ticket in tickets_data
            ]
            for ticket in tickets:
                ticket.full_clean()

            Ticket.objects.bulk_create(tickets)

            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
