from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


from . import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profil_handler(sender, instance, created, **kwargs):
    if not created:
        return

    # Create Only if is a new one
    profil = models.Profil(user=instance)
    profil.save()


@receiver(post_save, sender=models.Test)
def create_testplus(sender, instance, created, **kwargs):
    if not created:
        return

    test_plus = models.TestPlus(name=instance.name)
    test_plus.save()
