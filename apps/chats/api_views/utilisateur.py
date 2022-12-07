import os
from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response

from .. import models, serializers
from . import auth_response


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
        print (request.META['SERVER_PORT'])
        headers = self.get_success_headers(serializer.data)
        PORT = os.environ.get('SERVER_PORT', 'DEFAULT ONE')
        
        return Response({"response": response, "PORT" : PORT}, status=status.HTTP_201_CREATED, headers=headers)
