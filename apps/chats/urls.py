from django.urls import path, include

# rest_framework
from rest_framework.routers import DefaultRouter

# application
# from .views import index
from .api_views import ProfilApiViewSet, TestApiViewSet


router = DefaultRouter()
router.register("profils", ProfilApiViewSet)
router.register("tests", TestApiViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
]
