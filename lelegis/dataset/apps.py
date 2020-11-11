from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(AppConfig):
    name = 'lelegis.dataset'
    label = 'dataset'
    verbose_name = _('Conjunto de Busca')
