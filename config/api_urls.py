from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chats import api_views

router = DefaultRouter()
router.register('utilisateurs', api_views.UtilisateurListApiViewSet)

# utilisateurs = api_views.UtilisateurListApiViewSet.as_view({
#     'get': 'list',

# })
# utilisateur = api_views.UtilisateurListApiViewSet.as_view({
#     'get': 'retrieve',
# })

urlpatterns = [
    path('api/', include(router.urls)),
]
