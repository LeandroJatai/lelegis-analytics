
from django import template
from django.utils.safestring import mark_safe
from webpack_loader import utils


register = template.Library()


@register.simple_tag
def render_chunk_vendors(extension=None):
    try:
        tags = utils.get_as_tags(
            'chunk-vendors', extension=extension, config='DEFAULT', attrs='')
        return mark_safe('\n'.join(tags))
    except:
        return ''
