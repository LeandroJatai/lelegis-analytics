from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiConfig(AppConfig):
    name = 'api'
    label = 'api'
    verbose_name = _('Api LelegisAnalytics')
