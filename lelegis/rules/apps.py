from builtins import LookupError
import logging

import django.apps
from django.contrib.auth.management import _get_all_permissions
from django.core import exceptions
from django.db import router
from django.db.models.signals import post_migrate
from django.db.utils import DEFAULT_DB_ALIAS
from django.dispatch.dispatcher import receiver
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _


class AppConfig(django.apps.AppConfig):
    name = 'lelegis.rules'
    label = 'rules'
    verbose_name = _('Regras de Acesso')


@receiver(post_migrate, dispatch_uid='django.contrib.auth.management.create_permissions')
def create_proxy_permissions(
        app_config, verbosity=2, interactive=True,
        using=DEFAULT_DB_ALIAS, **kwargs):
    if not app_config.models_module:
        return
    logger = logging.getLogger(__name__)
    # print(app_config)

    try:
        logger.info("Tentando obter modelo de permissão do app.")
        Permission = django.apps.apps.get_model('auth', 'Permission')
    except LookupError as e:
        logger.error(str(e))
        return

    if not router.allow_migrate_model(using, Permission):
        return

    from django.contrib.contenttypes.models import ContentType

    permission_name_max_length = Permission._meta.get_field('name').max_length

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in list(app_config.get_models()):
        opts = klass._meta
        permissions = (
            ("list_" + opts.model_name,
             format_lazy(
                 '{} {}',
                 _('Visualizaçao da lista de'),
                 opts.verbose_name_plural)
             ),
            ("detail_" + opts.model_name,
             format_lazy(
                 '{} {}',
                 _('Visualização dos detalhes de'),
                 opts.verbose_name_plural)
             ),
        )
        opts.permissions = tuple(
            set(list(permissions) + list(opts.permissions)))

        if opts.proxy:
            # Force looking up the content types in the current database
            # before creating foreign keys to them.
            app_label, model = opts.app_label, opts.model_name

            try:
                logger.info("Tentando obter db_manager.")
                ctype = ContentType.objects.db_manager(
                    using).get_by_natural_key(app_label, model)
            except Exception as e:
                logger.error(str(e))
                ctype = ContentType.objects.db_manager(
                    using).create(app_label=app_label, model=model)
        else:
            ctype = ContentType.objects.db_manager(using).get_for_model(klass)

        ctypes.add(ctype)

        _all_perms_of_klass = _get_all_permissions(klass._meta)

        for perm in _all_perms_of_klass:
            searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(Permission.objects.using(using).filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    perms = [
        Permission(codename=codename, name=name, content_type=ct)
        for ct, (codename, name) in searched_perms
        if (ct.pk, codename) not in all_perms
    ]
    # Validate the permissions before bulk_creation to avoid cryptic database
    # error when the name is longer than 255 characters
    for perm in perms:
        if len(perm.name) > permission_name_max_length:
            logger.error("The permission name %s of %s.%s "
                         "is longer than %s characters" % (
                             perm.name,
                             perm.content_type.app_label,
                             perm.content_type.model,
                             permission_name_max_length,
                         ))
            raise exceptions.ValidationError(
                'The permission name %s of %s.%s '
                'is longer than %s characters' % (
                    perm.name,
                    perm.content_type.app_label,
                    perm.content_type.model,
                    permission_name_max_length,
                )
            )
    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)


def get_rules():
    from lelegis.rules.map_rules import rules_patterns
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    class Rules:

        def __init__(self, rules_patterns):
            self.rules_patterns = rules_patterns

        def associar(self, g, model, tipo):
            for t in tipo:
                content_type = ContentType.objects.get_by_natural_key(
                    app_label=model._meta.app_label,
                    model=model._meta.model_name)

                codename = (t[1:] + model._meta.model_name)\
                    if t[0] == '.' and t[-1] == '_' else t

                p = Permission.objects.get(
                    content_type=content_type,
                    codename=codename)
                g.permissions.add(p)
            g.save()

        def _config_group(self, group_name, rules_list):
            if not group_name:
                return
            logger = logging.getLogger(__name__)
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()

            try:
                logger.info("Tentando associar grupos.")
                print(' ', group_name)
                for model, perms, perms_publicas in rules_list:
                    self.associar(group, model, perms)
            except Exception as e:
                logger.error(str(e))
                print(group_name, e)

        def groups_add_user(self, user, groups_name):
            if not isinstance(groups_name, list):
                groups_name = [groups_name, ]
            for group_name in groups_name:
                if not group_name or user.groups.filter(
                        name=group_name).exists():
                    continue
                g = Group.objects.get_or_create(name=group_name)[0]
                user.groups.add(g)

        def groups_remove_user(self, user, groups_name):
            if not isinstance(groups_name, list):
                groups_name = [groups_name, ]
            for group_name in groups_name:
                if not group_name or not user.groups.filter(
                        name=group_name).exists():
                    continue
                g = Group.objects.get_or_create(name=group_name)[0]
                user.groups.remove(g)

        def update_groups(self):
            print('')
            print(format_lazy('{}{}{}', '\033[93m\033[1m',
                              _('Atualizando grupos do LeLegis:'),
                              '\033[0m'))
            for rules_group in self.rules_patterns:
                group_name = rules_group['group']
                rules_list = rules_group['rules']
                self._config_group(group_name, rules_list)

    return Rules(rules_patterns)


@receiver(post_migrate, dispatch_uid='update_groups')
def update_groups(app_config, verbosity=2, interactive=True,
                  using=DEFAULT_DB_ALIAS, **kwargs):
    if app_config != AppConfig and not isinstance(app_config, AppConfig):
        return
    rules = get_rules()
    rules.update_groups()
