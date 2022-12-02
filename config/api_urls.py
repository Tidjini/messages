from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chats import api_views

router = DefaultRouter()
router.register('utilisateurs', api_views.UtilisateurListApiViewSet)
router.register('discussions', api_views.DiscussionApiViewSet)
router.register('messages', api_views.MessageApiViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/token/', api_views.AuthenticationAPI.token,
         name='Token Authentication'),
    path('api/auth/username/', api_views.AuthenticationAPI.username,
         name='Username Authentication')
]
