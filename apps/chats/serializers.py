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


class MessageSerializer(ModelSerializerMixin):

    receiver = serializers.SerializerMethodField()
    send_to = UtilisateurSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id",)

    def get_receiver(self, obj):
        receiver = obj.receiver
        return UtilisateurSerializer(receiver).data


class DiscussionSerializer(ModelSerializerMixin):

    participants_count = serializers.ReadOnlyField()
    other = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = "__all__"
        read_only_fields = ("id",)

    def get_other(self, obj):

        request = self.context['request']
        if request and hasattr(request, 'user'):
            other = obj.other(request.user)
            if other:
                return UtilisateurSerializer(other).data
        return None

    def get_last_message(self, obj):
        last = obj.last_message
        if last:
            return MessageSerializer(last).data
        return None


# todo custom this notification to be send with discussion item
# Todo switch to english in applications

class MessageNotificationSerializer(ModelSerializerMixin):

    receiver = serializers.SerializerMethodField()
    send_to = UtilisateurSerializer(source='sender', read_only=True)
    # room = DiscussionSerializer(source='discussion', read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id",)

    def get_receiver(self, obj):
        receiver = obj.receiver
        return UtilisateurSerializer(receiver).data
