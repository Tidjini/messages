from rest_framework import viewsets, permissions, filters

from . import models, serilizers


class UtilisateurApiViewSet(viewsets.ModelViewSet):

    queryset = models.Utilisateur.objects.all()
    serializer_class = serilizers.UtilisateurSerializer
    permission_classes = (permissions.AllowAny,)
    # try this
    # filter_backends = [filters.OrderingFilter]
    ordering_fields = 'name', 'telephone', 'exercice'
