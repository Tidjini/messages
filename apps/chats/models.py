import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.hashers import check_password


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Utilisateur(AbstractBaseUser, TimeStampedModel):
    # override primary key with char key, review for UUID
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=30, unique=True)
    nom = models.CharField(max_length=30, null=False, blank=False)
    prenom = models.CharField(max_length=30, null=False, blank=False)
    sex = models.IntegerField(default=1)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    photo = models.ImageField(null=True, max_length=1024)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    telephone_deux = models.CharField(max_length=20, null=True, blank=True)
    # as react with fuse
    # role = ArrayField(
    #     models.CharField(max_length=50, blank=True, null=True), blank=True, default=list
    # )

    date_naissance = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nom", "prenom"]

    # travail sur une base de données spécifier
    database_name = models.CharField(max_length=50, null=True, blank=True)
    # work on exercice by year 2021 (id)
    exercice = models.CharField(max_length=100, null=True, blank=True)
    # authorize to work on
    # database_authorized = ArrayField(
    #     models.CharField(max_length=50, blank=True, null=True), blank=True, default=list
    # )

    def lower_data(self, *args):
        data = {k: v.lower() for k, v in self.__dictionary.items()
                if k in args and type(v) is str}
        rest = {k: v for k, v in self.__dictionary.items() if k not in args}
        data.update(rest)
        return data

    @property
    def __dictionary(self):
        field_names = [f.name for f in self._meta.fields]
        return {key: value for key, value in self.__dict__.items() if key in field_names}

    @property
    def __effective(self):
        field_names = [f.name for f in self._meta.fields]
        return {key: value for key, value in self.__dict__.items() if key in field_names and value}

    def create(self, *args, **kwargs):
        data = self.lower_data("username", "nom", "prenom")
        utilisateur = Utilisateur(**data)
        utilisateur.set_password(data["password"])
        utilisateur.is_staff = True
        super(Utilisateur, utilisateur).save(*args, **kwargs)

    def exist(self, *args):

        fields = {k: v for k, v in self.__dictionary.items() if k in args}
        try:
            return Utilisateur.objects.get(**fields)
        except Utilisateur.MultipleObjectsReturned:
            return Utilisateur.objects.filter(**fields)[0]
        except Utilisateur.DoesNotExist:
            return None

    def update(self, utilisateur):
        if utilisateur.check_password(self.password):
            values = self.__effective
            del values['id']
            return Utilisateur.objects.filter(pk=utilisateur.id).update(**values)

        raise Exception(
            "Username exist but password is wrong. check password or try other username"
        )

    def save(self,  *args, **kwargs):

        # todo later review this
        # if self.pk:
        #     super(Utilisateur, self).save(*args, **kwargs)
        self.username = self.username.lower()
        utilisateur = self.exist("username")
        if utilisateur:
            return self.update(utilisateur)
        self.create(*args, **kwargs)

    def __str__(self):

        return "username:{}, nom:{}".format(self.username, self.nom)
