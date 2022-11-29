# drf
from rest_framework import viewsets, permissions

# application
from .models import Profil, Test
from .serializers import ProfilSerializer, TestSerializer


class ProfilApiViewSet(viewsets.ModelViewSet):

    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = (permissions.AllowAny,)


class TestApiViewSet(viewsets.ModelViewSet):

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (permissions.AllowAny,)
