
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from lelegis.api.views import ApiViewSetConstrutor

from .apps import AppConfig


app_name = AppConfig.name


router = DefaultRouter()

for app, built_sets in ApiViewSetConstrutor._built_sets.items():
    for view_prefix, viewset in built_sets.items():
        router.register(app.label + '/' +
                        view_prefix._meta.model_name, viewset)


urlpatterns_router = router.urls


urlpatterns = [
    url(r'^api/', include(urlpatterns_router)),

]
