from rest_framework import serializers

from . import models


class UtilisateurSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = models.Utilisateur
        fields = '__all__'
        read_only_fields = 'id',
