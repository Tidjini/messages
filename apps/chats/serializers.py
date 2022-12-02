from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Utilisateur, Discussion, Message


class ModelSerializerMixin(serializers.ModelSerializer):
    def clean_validate_data_keys(self, *keys):
        """Clean Data
        keys: Specific Keys to clean
        Clean extensions fields from validated data to be conform with model fields"""
        for key in keys:
            if key in self._validated_data:
                del self._validated_data[key]

    def clean_validate_data(self):
        """Clean Data, to match  the model fields

        Clean extensions fields from validated data to be conform with model fields"""
        self._validated_data = {
            key: value
            for key, value in self._validated_data.items()
            if key in self.Meta.model.keys()
        }


class UtilisateurSerializer(ModelSerializerMixin):
    name = serializers.ReadOnlyField()
    password_one = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    password_two = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    def save(self, **kwargs):
        pwd_one, pwd_two = [
            value
            for key, value in self.validated_data.items()
            if key in ("password_one", "password_two")
        ]
        # check passwords confromity
        if pwd_one != pwd_two:
            raise ValidationError("Passwords not matched, retry again")

        self.clean_validate_data()
        self._validated_data.update(password=pwd_one)

        try:
            return super().save(**kwargs)
        except ValueError as e:
            raise ValidationError(
                "Passwords not matched with original password, retry again"
            )

    class Meta:
        model = Utilisateur
        exclude = ("password",)
        read_only_fields = ("id",)


class DiscussionSerializer(ModelSerializerMixin):
    class Meta:
        model = Discussion
        fields = "__all__"
        read_only_fields = ("id",)


class MessageSerializer(ModelSerializerMixin):
    
    receiver = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id",)
