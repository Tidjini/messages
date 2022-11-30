from django.test import TestCase
from django.conf import settings

from . import models


class UtilisateurTestCase(TestCase):

    def setUp(self):
        # is lower checking
        # replace old user, if has same username and password
        user = models.Utilisateur(
            username='AMine', nom='Amine', prenom='Samir', password='1234')
        user.save()

    def test_lowercase(self):

        user = models.Utilisateur.objects.get(username='amine')
        self.assertEqual(user.username.islower(), True)
        self.assertEqual(user.nom.islower(), True)
        self.assertEqual(user.prenom.islower(), True)

    def test_existance(self):
        user_exist = models.Utilisateur(
            username='aminE', nom='Amin Ali Mohamed', password='1234')
        user_exist.save()
        user = models.Utilisateur.objects.get(username='amine')
        self.assertEqual(user_exist.nom, user.nom)
        self.assertEqual(models.Utilisateur.objects.count(), 1)

    def test_name(self):
        user = models.Utilisateur(
            username='aminE', nom='Messaoudi', prenom='tidjini')
        name = '{} {}'.format('messaoudi'.upper(), 'tidjini'.title())
        self.assertEqual(user.name, name)

    def test_username_auth(self):
        success = models.Utilisateur.username_auth(
            username='amiNe', password='1234')
        failed = models.Utilisateur.username_auth(
            username='amiNe', password='123_4')
        self.assertEqual(bool(success), True)
        self.assertEqual(bool(failed), False)
