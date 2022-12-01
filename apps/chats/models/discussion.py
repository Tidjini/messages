from django.db import models

from .mixins import TimeStampedModel
from .utilisateur import Utilisateur


# create discussion if not exist between atomic entities
class Discussion(TimeStampedModel):
    # for custom discussion with multiples users, use group type
    TYPES = (("s", "single"), ("g", "group"))
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=TYPES, default="s")

    @property
    def participants_count(self):
        return self.participants.all().count()


class Participant(models.Model):
    user = models.ForeignKey(
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
    user = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="my_messages",
    )
    message = models.TextField()


class MessageVue(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="vues")
    user = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name="mes_vues"
    )
