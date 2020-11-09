
from lelegis.rules import (RP_ADD, RP_CHANGE, RP_DELETE, RP_DETAIL, RP_LIST,
                           GROUP_ANONYMOUS, GROUP_LOGIN_SOCIAL)


__base__ = [RP_LIST, RP_DETAIL, RP_ADD, RP_CHANGE, RP_DELETE]
__listdetailchange__ = [RP_LIST, RP_DETAIL, RP_CHANGE]

__perms_publicas__ = {RP_LIST, RP_DETAIL}


# não possui efeito e é usada nos testes que verificam se todos os models estão
# neste arquivo rules.py
rules_group_anonymous = {
    'group': GROUP_ANONYMOUS,
    'rules': [
    ]
}

rules_group_login_social = {
    'group': GROUP_LOGIN_SOCIAL,
    'rules': []
}

rules_patterns = [
    rules_group_anonymous,   # anotação para validação do teste de rules
    rules_group_login_social  # TODO não implementado
]


rules_patterns_public = {}


def _get_registration_key(model):
    return '%s:%s' % (model._meta.app_label, model._meta.model_name)


for rules_group in rules_patterns:
    for rules in rules_group['rules']:
        key = _get_registration_key(rules[0])
        if key not in rules_patterns_public:
            rules_patterns_public[key] = set()

        r = set(map(lambda x, m=rules[0]: '{}{}{}'.format(
            m._meta.app_label,
            x,
            m._meta.model_name), rules[2]))
        rules_patterns_public[key] = rules_patterns_public[key] | r
