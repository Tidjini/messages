from django.db import models


class ModelUtilsMixin(models.Model):

    @property
    def keys(self):
        _keys = [f.name for f in self._meta.fields]
        return _keys

    @property
    def dictionary(self):
        return {
            key: value for key, value in self.__dict__.items() if key in self.keys
        }

    @property
    def value_dict(self):
        return {
            key: value
            for key, value in self.dictionary.items()
            if key in self.keys and value
        }

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_modification = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
