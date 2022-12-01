from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chats.api_views import UtilisateurListApiViewSet, AuthenticationAPI, DiscussionAPI

router = DefaultRouter()
router.register('utilisateurs', UtilisateurListApiViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/token/', AuthenticationAPI.token,
         name='Token Authentication'),
    path('api/auth/username/', AuthenticationAPI.username,
         name='Username Authentication'),

    path('api/discussion/create/',
         DiscussionAPI.create_discussion, name='create discussion')
]
