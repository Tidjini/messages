from django.db import models


class ModelUtilsMixin(models.Model):

    @classmethod
    def keys(cls):
        _keys = [f.name for f in cls._meta.fields]
        return _keys

    @property
    def dictionary(self):
        return {
            key: value for key, value in self.__dict__.items() if key in self.keys()
        }

    @property
    def value_dict(self):
        return {
            key: value
            for key, value in self.dictionary.items()
            if key in self.keys() and value
        }

    def lower_data(self, *args):
        data = {
            k: v.lower()
            for k, v in self.dictionary.items()
            if k in args and type(v) is str
        }
        rest = {k: v for k, v in self.dictionary.items() if k not in args}
        data.update(rest)
        return data

    def exist(self, *args):
        fields = {k: v for k, v in self.dictionary.items() if k in args}
        try:
            return self.__class__.objects.get(**fields)
        except self.__class__.MultipleObjectsReturned:
            # todo review this in some cases
            return self.model_class.objects.filter(**fields)[0]
        except self.__class__.DoesNotExist:
            return None

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_modification = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
