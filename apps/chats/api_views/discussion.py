
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from ..models import Utilisateur, Discussion


class DiscussionAPI:

    @api_view(('POST',))
    @permission_classes((permissions.IsAuthenticated,))
    @staticmethod
    def create_discussion(request, *args, **kwargs):

        creator: Utilisateur = request.user
        user_id = request.data.get('user', None)
        if not user_id:
            return Response('Users for discussion not exists', status=status.HTTP_204_NO_CONTENT)

        try:
            user = Utilisateur.objects.get(id=user_id)

        except Utilisateur.DoesNotExist:
            return Response('User Does not exist', status=status.HTTP_204_NO_CONTENT)
        except Utilisateur.MultipleObjectsReturned:
            return Response('Multiple Users Returned Contact the admin', status=status.HTTP_204_NO_CONTENT)
        # cheking
        creator_discussions = [d for d, *_ in creator.single_discussions]
        user_discussions = [d for d, *_ in user.single_discussions]
        common_discussion = [
            item for item in creator_discussions if item in user_discussions]

        if common_discussion:
            id = common_discussion[0]
            try:
                discussion = Discussion.objects.get(id=id)
                return Response('RETURN DISCUSSION')
            except Discussion.DoesNotExist:
                pass
            except Discussion.MultipleObjectsReturned:
                # todo make sure of this one, filter and return ?
                pass

        # create an new one

        # for id in common_discussion:
        #     try:
        #         discussion = Discussion.objects.get(id=id)
        #     except:
        #         continue

        #     if discussion.participants_count == 2:
        #         exist = discussion
        #         break

        # if exist is not None:
        #     return {}

        # create one
