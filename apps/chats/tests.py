import time
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.hashers import check_password

from . import models


class UtilisateurTestCase(TestCase):

    def setUp(self):
        pass
        # is lower checking
        # replace old user, if has same username and password
        # user = models.Utilisateur(
        #     username='AMine', nom='Amine', prenom='Samir', password='1234')

        # user.save()

    # def test_lowercase(self):

    #     user = models.Utilisateur.objects.get(username='amine')
    #     self.assertEqual(user.username.islower(), True)
    #     self.assertEqual(user.nom.islower(), True)
    #     self.assertEqual(user.prenom.islower(), True)

    # def test_existance(self):
    #     user_exist = models.Utilisateur(
    #         username='aminE', nom='Amin Ali Mohamed', password='1234')
    #     user_exist.save()
    #     user = models.Utilisateur.objects.get(username='amine')

    #     self.assertEqual(user_exist.id, user.id)
    #     self.assertEqual(user_exist.nom, user.nom)
    #     self.assertEqual(models.Utilisateur.objects.count(), 1)

    # def test_name(self):
    #     user = models.Utilisateur(
    #         username='aminE', nom='Messaoudi', prenom='tidjini')
    #     name = '{} {}'.format('messaoudi'.upper(), 'tidjini'.title())
    #     self.assertEqual(user.name, name)

    # def test_username_auth(self):
    #     success = models.Utilisateur.username_auth(
    #         username='amiNe', password='1234')
    #     failed = models.Utilisateur.username_auth(
    #         username='amiNe', password='123_4')
    #     self.assertEqual(bool(success), True)
    #     self.assertEqual(bool(failed), False)

    # def test_discussion(self):

    #     user = models.Utilisateur(
    #         username='AMine', nom='Amine', prenom='Samir', password='1234')

    #     disc_one = models.Discussion(name='room one')
    #     disc_two = models.Discussion(name='room two')

    #     user.save()
    #     disc_one.save()
    #     disc_two.save()

    #     part1 = models.Participant(user=user, discussion=disc_one)
    #     part2 = models.Participant(user=user, discussion=disc_two)

    #     part1.save()
    #     part2.save()

    #     # dis = [id for id, *_ in user.discussions]
    #     print(disc_one.participants_count)
    #     print([id for id in user.single_discussions])
    #     print([id for id in user.group_discussions])

    def test_discussion_other(self):

        user = models.Utilisateur(
            username='AMine', nom='Amine', prenom='Samir', password='1234')

        user2 = models.Utilisateur(
            username='Imad', nom='Amine', prenom='Samir', password='1234')

        disc_one = models.Discussion(name='room one')

        user.save()
        user2.save()
        disc_one.save()

        part1 = models.Participant(user=user, discussion=disc_one)
        part2 = models.Participant(user=user2, discussion=disc_one)
        message = models.Message(
            user=user2, discussion=disc_one, message="Message Content to TEST 1 ")
        message2 = models.Message(
            user=user, discussion=disc_one, message="Message Content to TEST 2 ")

        part1.save()
        part2.save()
        message.save()

        time.sleep(1)
        message2.save()

        # dis = [id for id, *_ in user.discussions]
        print(disc_one.other(user))
        print(disc_one.last_message)
