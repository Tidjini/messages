from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import JsonResponse
from rest_framework.authtoken.models import Token

from . import models, serializers


def auth_response(user, serializer):
    token = Token.objects.get(user=user)
    return {
        **serializer.data, 'token': token.key
    }


class UtilisateurListApiViewSet(viewsets.ModelViewSet):

    queryset = models.Utilisateur.objects.all()
    serializer_class = serializers.UtilisateurSerializer
    permission_classes = permissions.AllowAny,
    filter_backends = filters.OrderingFilter,
    ordering_fields = 'name', 'telephone', 'exercice'
    pagination_class = None

    def create(self, request, *args, **kwargs):
        # override create to send token to user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = auth_response(instance, serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


@api_view(('GET',))
@permission_classes((permissions.IsAuthenticated,))
def token_auth(request, *args, **kwargs):
    # set request header with Authorisation: token xxxxxxxxxxxxxx
    user = request.user
    serializer = serializers.UtilisateurSerializer(user)
    response = auth_response(user, serializer)
    return Response(response, status=status.HTTP_200_OK)
