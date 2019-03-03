
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.forms import MunicipioFilterSet, PesquisaFilterSet
from api.models import Municipio, CrawlerAction, PesquisaNode
from api.serializers import MunicipioSerializer, PesquisaSerializer


class PesquisaViewSet(ReadOnlyModelViewSet):
    serializer_class = PesquisaSerializer
    queryset = PesquisaNode.objects.all()
    filter_class = PesquisaFilterSet

    def list(self, request, *args, **kwargs):
        self.queryset = PesquisaNode.objects.filter(parent__isnull=True)
        return ReadOnlyModelViewSet.list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = PesquisaNode.objects.all()
        return ReadOnlyModelViewSet.retrieve(self, request, *args, **kwargs)


class MunicipioViewSet(ReadOnlyModelViewSet):
    serializer_class = MunicipioSerializer
    queryset = Municipio.objects.all()
    filter_class = MunicipioFilterSet

    @action(detail=False)
    def resumo_pais(self, request, *args, **kwargs):
        crawlers = CrawlerAction.objects.order_by(
            'municipio', '-date_test').distinct('municipio')

        pings = crawlers.values_list('ping_success', flat=True)

        fails = len(list(filter(lambda x: not x, pings)))
        valids = len(list(filter(lambda x: x, pings)))

        casas = CrawlerAction.objects.order_by(
            'municipio', '-date_test').distinct(
                'municipio').values_list('json_casalegislativa', flat=True)

        # Uma casa que respondeu e possui registro em base/casalegislativa
        configuradas = len(
            list(filter(lambda x: len(x) > 0 and 'error' not in x[0], casas)))

        results = [
            ('fails', fails),
            ('valids', valids),
            ('totals', fails + valids),
            ('configs', configuradas)
        ]

        return Response(results)
