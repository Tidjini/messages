from django.db import models
from django.conf import settings


class Test(models.Model):
    name = models.TextField()


class TestPlus(models.Model):
    name = models.TextField()


class Profil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    birthdate = models.DateField(null=True)


class TimespanModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(TimespanModel):
    sender = models.ForeignKey(
        Profil, on_delete=models.CASCADE, related_name="sended_messages"
    )
    message = models.TextField()


class MessageSend(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="sends")
    send_to = models.ForeignKey(
        Profil, on_delete=models.CASCADE, related_name="received_messages"
    )


class MessageView(TimespanModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="views")
    viewer = models.ForeignKey(
        Profil, on_delete=models.CASCADE, related_name="my_views"
    )
