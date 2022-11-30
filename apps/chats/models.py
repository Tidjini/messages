import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import check_password

# from django.contrib.postgres.fields import ArrayField todo install psycopg2
# for image field install pillow


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Utilisateur(AbstractBaseUser, TimeStampedModel):
    # override primary key with char key
    id = models.CharField(max_length=100, primary_key=True)
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

    @staticmethod
    def lower_data(keys, **kwargs):
        data = {k: v.lower() for k, v in kwargs.items() if k in keys and type(v) is str}
        rest = {k: v for k, v in kwargs.items() if k not in keys}
        data.update(rest)
        return data

    @classmethod
    def create(cls, using="default", *args, **kwargs):
        data = Utilisateur.lower_data(("username", "nom", "prenom"), kwargs)
        utilisateur = Utilisateur(**data)
        utilisateur.set_password(data["password"])
        utilisateur.is_staff = True
        return utilisateur.save(using=using)

    @classmethod
    def exist(cls, keys, **kwargs):
        # todo set this method in base model class
        fields = {k: v for k, v in kwargs.items() if k in keys}

        try:
            return cls.objects.get(**fields)
        except cls.MultipleObjectsReturned:
            return cls.objects.filter(**fields)[0]
        except cls.DoesNotExist:
            return None

    def save(self, using="default", *args, **kwargs):
        if self.pk:
            return super(Utilisateur, self).save(*args, **kwargs)

        utilisateur = Utilisateur.exist(("username",), **kwargs)
        if utilisateur:

            valide_pass = check_password(self.password, utilisateur.password)
            if valide_pass:
                return super(Utilisateur, utilisateur).save(*args, **kwargs)

            raise Exception(
                "Username exist but password is wrong. check password or try other username"
            )

        return Utilisateur.create(using, *args, **kwargs)

    def __str__(self):
        return "username:{}, nom:{}".format(self.username, self.nom)
