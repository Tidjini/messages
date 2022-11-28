# drf
from rest_framework import viewsets, permissions

# application
from .models import Profil
from .serializers import ProfilSerializer


class ProfilApiViewSet(viewsets.ModelViewSet):

    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = (permissions.AllowAny,)
