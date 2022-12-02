from rest_framework import viewsets, mixins, permissions, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from ..models import Utilisateur, Discussion, Participant, Message
from ..serializers import DiscussionSerializer, MessageSerializer


class DiscussionApiViewSet(viewsets.ModelViewSet):

    queryset = Discussion.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DiscussionSerializer

    
    def create(self, request, *args, **kwargs):
        return self.create_discussion(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        self.queryset = Discussion.objects.filter(participants__user=user).order_by('id')
        return super().list(request, *args, **kwargs)
        


        



    @staticmethod
    def get_user(id, *args, **kwargs):
        try:
            return Utilisateur.objects.get(id=id)
        except Utilisateur.DoesNotExist:
            return None
        except Utilisateur.MultipleObjectsReturned:
            # more specifications
            return None

    
    def response(self, instance, *args, **kwargs):
        serializer = self.get_serializer(instance)
        return Response(serializer.data, *args, **kwargs)

  
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


    def create_discussion(self, request, *args, **kwargs):

        creator: Utilisateur = request.user
        # get user by id
        user_id = request.data.get("user", None)
        if not user_id:
            return Response(
                "Users for discussion not exists", status=status.HTTP_204_NO_CONTENT
            )

        user = DiscussionApiViewSet.get_user(int(user_id))
        if user is None:
            return Response("User Does not exist", status=status.HTTP_204_NO_CONTENT)

        # check existance discussions
        disc_id = DiscussionApiViewSet.get_single_discussion(creator, user)

        if disc_id:
            try:
                discussion = Discussion.objects.get(id=disc_id)
                return self.response(
                    discussion, status=status.HTTP_200_OK
                )
            except Discussion.DoesNotExist:
                # continue to create a new one
                pass
            except Discussion.MultipleObjectsReturned:
                # return the first one
                discussion = Discussion.objects.filter(id=disc_id)[0]
                return self.response(
                    discussion, status=status.HTTP_200_OK
                )

        # todo custom name to get user A and B
        name = request.data.get("name", "discussion")

        discussion = Discussion.objects.create(name=name)
        Participant.objects.create(user=creator, discussion=discussion)
        Participant.objects.create(user=user, discussion=discussion)

        return self.response(
            discussion, status=status.HTTP_201_CREATED
        )



# class DiscussionApiViewSet(viewsets.GenericViewSet, mixins.)

class MessageApiViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

