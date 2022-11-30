from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import JsonResponse
from rest_framework.authtoken.models import Token

from . import models, serializers


class UtilisateurListApiViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Utilisateur.objects.all()
    serializer_class = serializers.UtilisateurSerializer
    permission_classes = permissions.AllowAny,
    filter_backends = filters.OrderingFilter,
    ordering_fields = 'name', 'telephone', 'exercice'
    pagination_class = None


@api_view(('POST',))
def create_utilisateur(request):
    utilisateur = models.Utilisateur(**request.data)
    try:
        utilisateur.save()
        token = Token.objects.get(user__id=utilisateur.pk)
        return Response({
            'utilisateur': serializers.UtilisateurSerializer(utilisateur).data,
            'token': token.key
        })
    except Exception as e:
        return Response({
            'code': 100,
            "message": f'Exception due to {e}'
        })
