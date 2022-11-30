import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# from django.contrib.postgres.fields import ArrayField todo install psycopg2
# for image field install pillow


class TimeStampedModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Utilisateur(AbstractBaseUser, TimeStampedModel):
    # override primary key with char key
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

    def save(self, *args, **kwargs):
        # check if exist
        # -> exist -> check pass -> matched -> save changes of data
        #                        -> else    -> return
        # -> else  -> create new one -> create Token object
        pass

    def __str__(self):
        return self.username
