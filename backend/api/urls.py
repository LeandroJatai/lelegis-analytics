
from django.urls import path
from api.views import EstadosViewSet

urlpatterns = [
    path('estados/', EstadosViewSet.as_view(), name="estado_api_list"),
]
