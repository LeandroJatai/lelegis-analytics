from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField, \
    PrimaryKeyRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer

from api.models import Municipio, PesquisaNode, Action, UF


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


class PingTrueSerializer(serializers.Serializer):
    pais = serializers.SerializerMethodField()
    regional = serializers.SerializerMethodField()
    estadual = serializers.SerializerMethodField()

    def get_pais(self, obj):
        # ping true
        pt = obj.action_set.filter(ping=True)
        return {
            'total': pt.count(),
            #'pagination': pt.filter(
            #    json__has_key='pagination',
            #    json__pagination__total_entries__gt=0
            #).count(),
            'results': pt.filter(
                json__has_key='results').exclude(
                json__results=[]).count()

        }

    def get_regional(self, obj):
        r = {}
        for regiao in Municipio.REGIAO_CHOICES:
            # filtro base
            fb = obj.action_set.filter(municipio__regiao=regiao[0])
            r[regiao[0]] = {
                'meta': regiao[1],
                'total': fb.filter(ping=True).count(),
                #'pagination': fb.filter(ping=True).filter(
                #    json__has_key='pagination',
                #    json__pagination__total_entries__gt=0
                #).count(),
                'results': fb.filter(ping=True).filter(
                    json__has_key='results'
                ).exclude(json__results=[]).count()
            }
        return r

    def get_estadual(self, obj):
        r = {}
        for uf in UF:
            # filtro base
            fb = obj.action_set.filter(municipio__uf=uf[0])
            r[uf[0]] = {
                'meta': uf[1],
                'total': fb.filter(ping=True).count(),
                #'pagination': fb.filter(ping=True).filter(
                #    json__has_key='pagination',
                #    json__pagination__total_entries__gt=0
                #).count(),
                'results': fb.filter(ping=True).filter(
                    json__has_key='results'
                ).exclude(json__results=[]).count()

            }
        return r


class PingFalseSerializer(serializers.Serializer):
    pais = serializers.SerializerMethodField()
    regional = serializers.SerializerMethodField()
    estadual = serializers.SerializerMethodField()

    def get_pais(self, obj):
        # ping false
        pf = obj.action_set.filter(ping=False)
        return {
            'total': pf.count(),
            #'content': pf.all().values_list('json', flat=True)
        }

    def get_regional(self, obj):
        r = {}
        for regiao in Municipio.REGIAO_CHOICES:
            # filtro base
            fb = obj.action_set.filter(
                municipio__regiao=regiao[0]).filter(ping=False)

            r[regiao[0]] = {
                'meta': regiao[1],
                'total': fb.count(),
            }
        return r

    def get_estadual(self, obj):
        r = {}
        for uf in UF:
            # filtro base
            fb = obj.action_set.filter(municipio__uf=uf[0]).filter(ping=False)

            r[uf[0]] = {
                'meta': uf[1],
                'false': fb.count(),
            }
        return r


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
