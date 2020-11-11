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


class PingMixin(serializers.Serializer):

    pais = serializers.SerializerMethodField()
    regional = serializers.SerializerMethodField()
    estadual = serializers.SerializerMethodField()

    def exec_choice(self, obj, params={}, sigla=None, meta=None):

        fb = obj.action_set.filter(ping=self.ping, **params)

        rr = {
            'total': fb.count(),
        }

        if sigla:
            rr['sigla'] = sigla

        if meta:
            rr['meta'] = meta

        if self.ping and obj.action_view:

            fbp = fb.filter(
                json__has_key='pagination')

            if fbp.exists():
                fbp = fbp.filter(
                    json__pagination__total_entries__gt=0
                )
                rr['has_entries'] = fbp.count()
            else:
                params['json__has_key'] = 'results'
                params['json__results__isnull'] = False
                rr['results'] = fb.filter(**params).count()
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


class PingTrueSerializer(PingMixin):
    ping = True


class PingFalseSerializer(PingMixin):
    ping = False


class PesquisaSerializer(serializers.ModelSerializer):
    ping_true = serializers.SerializerMethodField()
    ping_false = serializers.SerializerMethodField()

    childs = PrimaryKeyRelatedField(read_only=True, many=True)
    #action_set = ActionSerializer(many=True)

    class Meta:
        model = PesquisaNode
        fields = '__all__'

    def get_ping_true(self, obj):
        data = PingTrueSerializer(obj).data
        return data

    def get_ping_false(self, obj):
        data = PingFalseSerializer(obj).data
        return data
