from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chats.api_views import UtilisateurListApiViewSet, AuthenticationAPI

router = DefaultRouter()
router.register('utilisateurs', UtilisateurListApiViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/token/', AuthenticationAPI.token,
         name='token authentication'),
    path('api/auth/username/', AuthenticationAPI.username,
         name='token authentication')
]
