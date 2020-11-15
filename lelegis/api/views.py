import logging

from django import apps
from django.conf import settings
from django.urls.base import reverse
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import serializers as rest_serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from lelegis.api.forms import FilterSetMixin
from lelegis.dataset.models import Action, PesquisaNode


class BusinessRulesNotImplementedMixin:
    def create(self, request, *args, **kwargs):
        raise Exception(_("POST Create não implementado"))

    def update(self, request, *args, **kwargs):
        raise Exception(_("PUT and PATCH não implementado"))

    def delete(self, request, *args, **kwargs):
        raise Exception(_("DELETE Delete não implementado"))


class ApiViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)


class ApiViewSetConstrutor():

    _built_sets = {}

    @classonlymethod
    def get_class_for_model(cls, model):
        return cls._built_sets[model._meta.app_config][model]

    @classonlymethod
    def build_class(cls):
        import inspect
        from lelegis.api import serializers

        # Carrega todas as classes de project.api.serializers que possuam
        # "Serializer" como Sufixo.
        serializers_classes = inspect.getmembers(serializers)
        serializers_classes = {i[0]: i[1] for i in filter(
            lambda x: x[0].endswith('Serializer'),
            serializers_classes
        )}

        # Carrega todas as classes de project.api.forms que possuam
        # "FilterSet" como Sufixo.
        from lelegis.api import forms
        filters_classes = inspect.getmembers(forms)
        filters_classes = {i[0]: i[1] for i in filter(
            lambda x: x[0].endswith('FilterSet') and x[0] != 'FilterSet',
            filters_classes
        )}

        built_sets = {}

        def build(_model):
            object_name = _model._meta.object_name

            # Caso Exista, pega a classe project.api.serializers.{model}Serializer
            # ou utiliza a base do drf para gerar uma automática para o model
            serializer_name = f'{object_name}Serializer'
            _serializer_class = serializers_classes.get(
                serializer_name, rest_serializers.ModelSerializer)

            # Caso Exista, pega a classe sapl.api.forms.{model}FilterSet
            # ou utiliza a base definida em sapl.forms.SaplFilterSetMixin
            filter_name = f'{object_name}FilterSet'
            _filter_class = filters_classes.get(
                filter_name, FilterSetMixin)

            def create_class():

                _meta_serializer = object if not hasattr(
                    _serializer_class, 'Meta') else _serializer_class.Meta

                # Define uma classe padrão para serializer caso não tenha sido
                # criada a classe sapl.api.serializers.{model}Serializer
                class ApiSerializer(_serializer_class):
                    __str__ = SerializerMethodField()
                    link_detail_backend = rest_serializers.SerializerMethodField()

                    def get_link_detail_backend(self, obj):
                        try:
                            return reverse(f'{self.Meta.model._meta.app_config.name}:{self.Meta.model._meta.model_name}_detail',
                                           kwargs={'pk': obj.pk})
                        except:
                            return ''

                    class Meta(_meta_serializer):
                        if not hasattr(_meta_serializer, 'model'):
                            model = _model

                        if hasattr(_meta_serializer, 'exclude'):
                            exclude = _meta_serializer.exclude
                        else:
                            if not hasattr(_meta_serializer, 'fields'):
                                fields = '__all__'
                            elif _meta_serializer.fields != '__all__':
                                fields = list(
                                    _meta_serializer.fields) + ['__str__', ]
                            else:
                                fields = _meta_serializer.fields

                    def get___str__(self, obj):
                        return str(obj)

                _meta_filterset = object if not hasattr(
                    _filter_class, 'Meta') else _filter_class.Meta

                # Define uma classe padrão para filtro caso não tenha sido
                # criada a classe sapl.api.forms.{model}FilterSet
                class ApiFilterSet(_filter_class):
                    class Meta(_meta_filterset):
                        if not hasattr(_meta_filterset, 'model'):
                            model = _model

                # Define uma classe padrão ModelViewSet de DRF
                class ModelSaplViewSet(ApiViewSet):
                    queryset = _model.objects.all()

                    # Utiliza o filtro customizado pela classe
                    # sapl.api.forms.{model}FilterSet
                    # ou utiliza o trivial SaplFilterSet definido acima
                    filter_class = ApiFilterSet

                    # Utiliza o serializer customizado pela classe
                    # sapl.api.serializers.{model}Serializer
                    # ou utiliza o trivial SaplSerializer definido acima
                    serializer_class = ApiSerializer

                return ModelSaplViewSet

            viewset = create_class()
            viewset.__name__ = '%sModelSaplViewSet' % _model.__name__
            return viewset

        apps_project = [apps.apps.get_app_config(
            n.split('.')[-1]) for n in settings.APPS_PROJECT]
        for app in apps_project:
            cls._built_sets[app] = {}
            for model in app.get_models():
                cls._built_sets[app][model] = build(model)


ApiViewSetConstrutor.build_class()

"""
1. Constroi uma rest_framework.viewsets.ModelViewSet para 
   todos os models de todas as apps do projeto
2. Define DjangoFilterBackend como ferramenta de filtro dos campos
3. Define Serializer como a seguir:
    3.1 - Define um Serializer genérico para cada módel
    3.2 - Recupera Serializer customizado em [project].api.serializers
    3.3 - Para todo model é opcional a existência de 
          [project].api.serializers.{model}Serializer.
          Caso não seja definido um Serializer customizado, utiliza-se o trivial
4. Define um FilterSet como a seguir:
    4.1 - Define um FilterSet genérico para cada módel
    4.2 - Recupera FilterSet customizado em [project].api.forms
    4.3 - Para todo model é opcional a existência de 
          [project].api.forms.{model}FilterSet.
          Caso não seja definido um FilterSet customizado, utiliza-se o trivial
    4.4 - todos os campos que aceitam lookup 'exact' 
          podem ser filtrados por default
    
5. ApiViewSetConstrutor não cria padrões e/ou exige conhecimento alem dos
    exigidos pela DRF. 
    
6. As rotas são criadas seguindo nome da app e nome do model
    http://localhost:9000/api/{applabel}/{model_name}/
    e seguem as variações definidas em:
    https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    
7. Todas as viewsets construídas por ApiViewSetConstrutor e suas rotas
    (paginate list, detail, edit, create, delete)
   bem como testes em ambiente de desenvolvimento podem ser conferidas em:
   http://localhost:9000/api/ 
   desde que settings.DEBUG=True

**ApiViewSetConstrutor._built_sets** é um dict de dicts de models conforme:
    {
        ...
    
        'audiencia': {
            'tipoaudienciapublica': TipoAudienciaPublicaViewSet,
            'audienciapublica': AudienciaPublicaViewSet,
            'anexoaudienciapublica': AnexoAudienciaPublicaViewSet
            
            ...
            
            },
            
        ...
        
        'base': {
            'casalegislativa': CasaLegislativaViewSet,
            'appconfig': AppConfigViewSet,
            
            ...
            
        }
        
        ...
        
    }
"""

# Toda Classe construida acima, pode ser redefinida e aplicado quaisquer
# das possibilidades para uma classe normal criada a partir de
# rest_framework.viewsets.ModelViewSet conforme exemplo para a classe autor

# decorator para recuperar e transformar o default


class customize(object):
    def __init__(self, model):
        self.model = model

    def __call__(self, cls):

        class _ApiViewSet(
            cls,
                ApiViewSetConstrutor._built_sets[
                    self.model._meta.app_config][self.model]
        ):
            pass

        if hasattr(_ApiViewSet, 'build'):
            _ApiViewSet = _ApiViewSet.build()

        ApiViewSetConstrutor._built_sets[
            self.model._meta.app_config][self.model] = _ApiViewSet
        return _ApiViewSet


@customize(Action)
class _ActionViewSet:
    pass


@customize(PesquisaNode)
class _PesquisaNodeViewSet:

    def list(self, request, *args, **kwargs):
        self.queryset = PesquisaNode.objects.filter(parent__isnull=True)
        return ReadOnlyModelViewSet.list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = PesquisaNode.objects.all()
        return ReadOnlyModelViewSet.retrieve(self, request, *args, **kwargs)
