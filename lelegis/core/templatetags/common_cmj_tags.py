

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from webpack_loader import utils
from webpack_loader.utils import _get_bundle

register = template.Library()


def get_as_tags(bundle_name, extension=None, config='DEFAULT', attrs=''):
    '''
    Get a list of formatted <script> & <link> tags for the assets in the
    named bundle.

    :param bundle_name: The name of the bundle
    :param extension: (optional) filter by extension, eg. 'js' or 'css'
    :param config: (optional) the name of the configuration
    :return: a list of formatted tags as strings
    '''

    bundle = _get_bundle(bundle_name, extension, config)
    tags = []
    for chunk in bundle:
        if chunk['name'].endswith(('.js', '.js.gz')):
            tags.append((
                '<script src="{0}" {1}></script>'
            ).format(chunk['url'], attrs))
        elif chunk['name'].endswith(('.css', '.css.gz')):
            tags.append((
                '<link type="text/css" href="{0}" rel="stylesheet" {1}/>'
            ).format(chunk['url'], attrs))
    return tags


@register.simple_tag
def render_bundle(bundle_name, extension=None, config='DEFAULT', attrs=''):
    tags = get_as_tags(bundle_name, extension=extension,
                       config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))


@register.simple_tag
def settings_key_tag(var_name):
    return getattr(settings, var_name)


@register.filter
def settings_key_filter(var_name):
    return getattr(settings, var_name)


@register.simple_tag
def render_chunk_vendors(extension=None):
    try:
        tags = utils.get_as_tags(
            'chunk-vendors', extension=extension, config='DEFAULT', attrs='')
        return mark_safe('\n'.join(tags))
    except Exception as e:
        return ''
