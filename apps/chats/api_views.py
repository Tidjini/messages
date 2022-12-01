from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import JsonResponse
from rest_framework.authtoken.models import Token

from . import models, serializers


class UtilisateurListApiViewSet(viewsets.ModelViewSet):

    queryset = models.Utilisateur.objects.all()
    serializer_class = serializers.UtilisateurSerializer
    permission_classes = permissions.AllowAny,
    filter_backends = filters.OrderingFilter,
    ordering_fields = 'name', 'telephone', 'exercice'
    pagination_class = None

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)

    #     # try to check two password

    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save()


# @api_view(('POST',))
# def create_utilisateur(request):
#     utilisateur = models.Utilisateur(**request.data)
#     try:
#         utilisateur.save()
#     except Exception as e:
#         return Response({
#             'code': 100,
#             "message": f'Exception due to {e}'
#         })

#     token = Token.objects.get(user=utilisateur)
#     return Response({
#         'utilisateur': serializers.UtilisateurSerializer(utilisateur).data,
#         'token': token.key
#     })


# def
