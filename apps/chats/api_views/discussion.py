from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from ..models import Utilisateur, Discussion, Participant, Message
from ..serializers import DiscussionSerializer


class DiscussionAPI:
    @staticmethod
    def get_user(id, *args, **kwargs):
        try:
            return Utilisateur.objects.get(id=id)
        except Utilisateur.DoesNotExist:
            return None
        except Utilisateur.MultipleObjectsReturned:
            # more specifications
            return None

    @staticmethod
    def response(instance, serializer, *args, **kwargs):
        serial: serializers.ModelSerializer = serializer(instance)
        return Response(serial.data, *args, **kwargs)

    @staticmethod
    def discussion_response(instance, *args, **kwargs):
        return DiscussionAPI.response(instance, DiscussionSerializer, *args, **kwargs)

    @staticmethod
    def get_single_discussion(user_a, user_b):
        # get discussions
        user_a_discussions = [d for d, *_ in user_a.single_discussions]
        user_b_discussions = [d for d, *_ in user_b.single_discussions]

        common_discussion = [
            item for item in user_a_discussions if item in user_b_discussions
        ]

        if not common_discussion:
            return None
        return common_discussion[0]

    @api_view(("POST",))
    @permission_classes((permissions.IsAuthenticated,))
    @staticmethod
    def create_discussion(request, *args, **kwargs):

        creator: Utilisateur = request.user

        # get user by id
        user_id = request.data.get("user", None)
        if not user_id:
            return Response(
                "Users for discussion not exists", status=status.HTTP_204_NO_CONTENT
            )

        user = DiscussionAPI.get_user(int(user_id))
        if user is None:
            Response("User Does not exist", status=status.HTTP_204_NO_CONTENT)

        # check existance discussions
        disc_id = DiscussionAPI.get_single_discussion(creator, user)

        if disc_id:
            try:
                discussion = Discussion.objects.get(id=disc_id)
                return DiscussionAPI.discussion_response(
                    discussion, status=status.HTTP_200_OK
                )
            except Discussion.DoesNotExist:
                # continue to create a new one
                pass
            except Discussion.MultipleObjectsReturned:
                # return the first one
                discussion = Discussion.objects.filter(id=disc_id)[0]
                return DiscussionAPI.discussion_response(
                    discussion, status=status.HTTP_200_OK
                )

        # todo custom name to get user A and B
        name = request.data.get("name", "discussion")

        discussion = Discussion.objects.create(name=name)
        Participant.objects.create(user=creator, discussion=discussion)
        Participant.objects.create(user=user, discussion=discussion)

        return DiscussionAPI.discussion_response(
            discussion, status=status.HTTP_201_CREATED
        )


class MessageApiViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
