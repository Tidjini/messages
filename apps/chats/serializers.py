from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class ModelSerializer(serializers.ModelSerializer):

    def clean_validate_data(self, *keys):
        for key in keys:
            if key in self._validated_data:
                del self._validated_data[key]


class UtilisateurSerializer(ModelSerializer):
    name = serializers.ReadOnlyField()
    password_one = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password_two = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def save(self, **kwargs):
        pwd_one, pwd_two = [value for key, value in self.validated_data.items() if key in (
            'password_one', 'password_two')]
        # check passwords confromity
        if pwd_one != pwd_two:
            raise ValidationError('Passwords not matched, retry again')

        self.clean_validate_data('password_one', 'password_two')

        self._validated_data.update(password=pwd_one)

        try:
            return super().save(**kwargs)
        except ValueError as e:
            raise ValidationError(
                'Passwords not matched with original password, retry again')

    class Meta:
        model = models.Utilisateur
        exclude = 'password',
        read_only_fields = 'id',
