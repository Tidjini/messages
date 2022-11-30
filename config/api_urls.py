
from rest_framework.routers import DefaultRouter

from apps.chats import api_views

router = DefaultRouter()

router.register('utilisateurs', api_views.UtilisateurApiViewSet)
