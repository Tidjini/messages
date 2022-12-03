from django.db import models
from django.db.models.query import Q

from .mixins import TimeStampedModel, ModelUtilsMixin
from .utilisateur import Utilisateur


# create discussion if not exist between atomic entities
class Discussion(TimeStampedModel, ModelUtilsMixin):
    # for custom discussion with multiples users, use group type
    TYPES = (("s", "single"), ("g", "group"))
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=TYPES, default="s")

    @property
    def participants_count(self):
        return self.participants.all().count()

    def other(self, user):
        others = self.participants.filter(~Q(user=user))
        if others:
            return others[0].user
        return None

    @property
    def last_message(self):
        return self.messages.order_by("-date_creation").first()


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

    def __str__(self):
        return self.user.name


# TODO CD MESSAGES with Authenticated user not all Crud
# TODO GET Messages of specific Discussion
# TODO Push Notification to Current Discussion / user Thread with signals
# TODO Implemeting the socketio with gevent
class Message(TimeStampedModel, ModelUtilsMixin):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="my_messages",
    )
    message = models.TextField()

    @property
    def receivers(self):
        # todo group discussion
        return []

    @property
    def receiver(self):
        return self.discussion.other(self.sender).id

    def __str__(self):
        return "{}-{} : {}".format(self.discussion.name, self.user.name, self.message)


class MessageVue(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="vues")
    user = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name="mes_vues"
    )
