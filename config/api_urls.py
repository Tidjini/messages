from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chats import api_views

router = DefaultRouter()
router.register('utilisateurs', api_views.UtilisateurListApiViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/utilisateur/create/', api_views.create_utilisateur,
         name='create_utilisateur')
]
