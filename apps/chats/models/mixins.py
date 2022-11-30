from django.db import models


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_modification = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
