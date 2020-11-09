import inspect
import json
import logging

from django.conf import settings
from django.core import serializers
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver

from lelegis.core.models import AuditLog


def audit_log_function(sender, **kwargs):

    try:
        app_name = sender._meta.app_config.name[:7]
        if app_name not in ('lelegis', ):
            return
    except:
        # não é necessário usar logger, aqui é usada apenas para
        # eliminar um o if complexo
        return

    instance = kwargs.get('instance')
    if instance._meta.model in (
        AuditLog,       # Causa recursividade
    ):
        return

    logger = logging.getLogger(__name__)

    u = None
    for i in inspect.stack():
        if i.function == 'migrate':
            return
        r = i.frame.f_locals.get('request', None)
        try:
            if r.user._meta.label == settings.AUTH_USER_MODEL:
                u = r.user
                if u.is_anonymous:
                    return
                break
        except:
            # não é necessário usar logger, aqui é usada apenas para
            # eliminar um o if complexo
            pass

    try:
        operation = kwargs.get('operation')
        al = AuditLog()
        al.user = u
        al.email = u.email if u else ''
        al.operation = operation
        al.obj = json.loads(serializers.serialize("json", (instance, )))
        al.content_object = instance if operation != 'D' else None
        al.obj_id = instance.id
        al.model_name = instance._meta.model_name
        al.app_name = instance._meta.app_label
        al.save()

    except Exception as e:
        logger.error('Error saving auditing log object')
        logger.error(e)


@receiver(post_delete)
def audit_log_post_delete(sender, **kwargs):
    audit_log_function(sender, operation='D', **kwargs)


@receiver(post_save)
def audit_log_post_save(sender, **kwargs):
    operation = 'C' if kwargs.get('created') else 'U'
    audit_log_function(sender, operation=operation, **kwargs)
