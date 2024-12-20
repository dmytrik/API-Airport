from rest_framework import serializers

from airport.models import Crew


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "full_name")
        read_only_fields = ("id",)
