# rest_framework
from rest_framework import serializers

# application
from .models import Profil, Test


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = "__all__"
        read_only_fields = ("id",)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        read_only_fields = ("id",)
