from django.utils.translation import ugettext_lazy as _

default_app_config = 'lelegis.rules.apps.AppConfig'

"""
Os cinco radicais de permissão completa são:

        RP_LIST, RP_DETAIL, RP_ADD, RP_CHANGE, RP_DELETE =\
            '.list_', '.detail_', '.add_', '.change_', '.delete_',

Tanto a app crud quanto a app rules estão sempre ligadas a um model. Ao lidar
com permissões, sempre é analisado se é apenas um radical ou permissão
completa, sendo apenas um radical, a permissão completa é montada com base
no model associado.
"""

RP_LIST, RP_DETAIL, RP_ADD, RP_CHANGE, RP_DELETE =\
    '.list_', '.detail_', '.add_', '.change_', '.delete_',

GROUP_LOGIN_SOCIAL = _("Usuários com Login Social")

# ANONYMOUS não é um grupo mas é uma variável usadas nas rules para anotar
# explicitamente models que podem ter ação de usuários anônimos
# como por exemplo AcompanhamentoMateria
GROUP_ANONYMOUS = ''

LELEGIS_GROUPS = [
    GROUP_LOGIN_SOCIAL,
    GROUP_ANONYMOUS,
]

MENU_PERMS_FOR_USERS = ()
