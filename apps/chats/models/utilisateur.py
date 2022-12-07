from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token

from .mixins import TimeStampedModel, ModelUtilsMixin


class Utilisateur(AbstractBaseUser, ModelUtilsMixin, TimeStampedModel):

    # override primary key with char key, review for UUID
    # id = models.IntegerField(primary_key=True, auto_created=True)
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

    def create(self, *args, **kwargs):
        data = self.lower_data("username", "nom", "prenom")
        self.set_password(data["password"])
        del data["password"]
        self.is_staff = True
        self.is_active = True
        self.__dict__.update(data)
        super(Utilisateur, self).save(*args, **kwargs)

    def exist_with_password(self, *args):
        existed_user = self.exist(*args)
        if existed_user and existed_user.check_password(self.password):
            return existed_user
        return None

    def update(self, old, *args, **kwargs):
        # this update all data come from user
        if old.check_password(self.password):
            # set old id to update
            self.id = old.id
            # set hashed password for old entity
            self.set_password(self.password)
            try:
                return super(Utilisateur, self).save(*args, **kwargs)
            except Exception as e:
                raise ValueError(f"Exception due to : {e}")

        raise ValueError(
            "Username exist but password is wrong. check password or try other username"
        )

    def save(self, *args, **kwargs):
        self.username = self.username.lower()

        old = self.exist("username")
        if old:
            return self.update(old, *args, **kwargs)

        self.create(*args, **kwargs)

    @property
    def name(self):
        return "{} {}".format(self.nom.upper(), self.prenom.title())

    @property
    def discussions(self):
        return self.participations.values_list('discussion')

    @property
    def single_discussions(self):
        return self.participations.filter(discussion__type='s').values_list('discussion')

    # todo for single discussion get other users
    # use managers for this

    @property
    def group_discussions(self):
        return self.participations.filter(discussion__type='g').values_list('discussion')

    @property
    def token_key(self):
        token = self.auth_token
        if token:
            return token.key
        return None

    def __str__(self):
        return "username:{}, nom:{}".format(self.username, self.nom)


class UtilisateurAPI:

    def username_auth(username, password, *args, **kwargs):
        user = Utilisateur(username=username.lower(), password=password)
        user = user.exist_with_password("username")
        # make sure is active
        if user and user.is_active:
            return user
        return None
