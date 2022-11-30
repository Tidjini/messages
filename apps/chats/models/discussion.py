from django.db import models

from .mixins import TimeStampedModel
from .utilisateur import Utilisateur


class Discussion(TimeStampedModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)


class Participant(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name="participations",
    )

    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="participants"
    )


class Message(TimeStampedModel):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="messages"
    )
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="my_messages",
    )
    message = models.TextField()


class MessageVue(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="vues")
    utilisateur = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name="mes_vues"
    )
