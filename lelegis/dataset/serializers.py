from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField, \
    PrimaryKeyRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer

from lelegis.dataset.models import Municipio, PesquisaNode, Action, UF


class ChoiceSerializer(serializers.Serializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj[1]

    def get_value(self, obj):
        return obj[0]


class MunicipioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipio
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'


class ExecSerializer(serializers.Serializer):

    pais = serializers.SerializerMethodField()
    regional = serializers.SerializerMethodField()
    estadual = serializers.SerializerMethodField()

    def exec_choice(self, obj, params={}, sigla=None, meta=None):

        qs = obj.action_set.filter(**params)

        rr = {
            'ping_true': {
                'has_entries': qs.filter(ping=True).count(),
                'count': qs.filter(ping=True).count(),
                'sigla': sigla,
                'meta': meta
            },
            'ping_false': {
                'has_entries': qs.filter(ping=False).count(),
                'count': qs.filter(ping=False).count(),
                'sigla': sigla,
                'meta': meta
            }
        }

        if obj.action_view:
            qs = qs.filter(ping=True)
            qss = qs.filter(
                json__has_key='pagination')

            if qss.exists():
                qss = qss.filter(
                    json__pagination__total_entries__gt=0
                )
                soma = 0
                for v in qss:
                    soma += v.json['pagination']['total_entries']
                rr['ping_true']['has_entries'] = qss.count()
                rr['ping_true']['size_entries'] = soma
            else:
                params['json__has_key'] = 'results'
                params['json__results__isnull'] = False

                rr['ping_true']['has_entries'] = qs.filter(**params).count()

                soma = 0
                for v in qs.filter(**params):
                    soma += len(v.json['results'])

                rr['ping_true']['size_entries'] = soma
                # if not rr['results']:
                #    rr['has_entries'] = fbp.count()

        return rr

    def get_pais(self, obj):
        return self.exec_choice(obj, params={})

    def get_regional(self, obj):
        for regiao in Municipio.REGIAO_CHOICES:
            params = {'municipio__regiao': regiao[0]}
            yield self.exec_choice(obj, params, regiao[0], regiao[1])

    def get_estadual(self, obj):
        for uf in UF:
            params = {'municipio__uf': uf[0]}
            yield self.exec_choice(obj, params, uf[0], uf[1])


class PesquisaSerializer(serializers.ModelSerializer):
    EXEC = serializers.SerializerMethodField()

    childs = PrimaryKeyRelatedField(read_only=True, many=True)
    #action_set = ActionSerializer(many=True)

    class Meta:
        model = PesquisaNode
        fields = '__all__'

    def get_EXEC(self, obj):
        return ExecSerializer(obj).data
