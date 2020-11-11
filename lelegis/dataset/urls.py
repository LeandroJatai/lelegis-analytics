
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from lelegis.dataset.views import MunicipioViewSet, PesquisaViewSet

router = DefaultRouter()
router.register(r'municipio', MunicipioViewSet)
router.register(r'pesquisa', PesquisaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
