from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from rest_framework.authtoken.models import Token
from .models.discussion import Message
from apps.communications.views import sio


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if not created:
        return
    # create token if is new one
    token = Token(user=instance)
    token.save()


@receiver(post_save, sender=Message)
def message_notification(sender, instance: Message, created, **kwargs):
    if not created:
        return
    
    # for participant in instance.discussion.other(user=instance.sender):
    participant = instance.discussion.other(user=instance.sender)
    if not participant or participant.token_key is None:
        return 

    print('=================send data to', participant.token_key)
    sio.emit(participant.token_key, {
        'message': instance.message
    })
