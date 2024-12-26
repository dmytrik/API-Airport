from rest_framework import serializers

from airport.models import Airplane


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "airplane_type")
        read_only_fields = ("id",)


class AirplaneListDetailSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)
