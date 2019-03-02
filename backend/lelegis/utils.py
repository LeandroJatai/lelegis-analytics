from django.apps.registry import apps
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin


def register_all_models_in_admin(module_name):
    appname = module_name.split('.')
    appname = appname[1] if appname[0] == 'lelegis' else appname[0]
    app = apps.get_app_config(appname)

    for model in app.get_models():

        class CustomModelAdmin(ModelAdmin):
            list_display = [f.name for f in model._meta.fields
                            if f.name != 'id']

        if not admin.site.is_registered(model):
            admin.site.register(model, CustomModelAdmin)
