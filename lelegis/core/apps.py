from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(AppConfig):
    name = 'lelegis.core'
    label = 'core'
    verbose_name = _('Ajustes Principais')
