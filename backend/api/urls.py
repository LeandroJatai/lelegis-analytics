
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from api.views import MunicipioViewSet

router = DefaultRouter()
router.register(r'municipio', MunicipioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
