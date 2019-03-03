import json
from platform import node
from time import sleep

from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count
from django.utils.text import slugify
import urllib3

from api.models import Municipio, CrawlerAction, PesquisaNode, Action


class Command(BaseCommand):

    def handle(self, *args, **options):
        """municipios = Municipio.objects.all().filter(
            nome__in=(
                'Jataí',
                'Formosa',
                'Ibiúna',
                'Agudo',
                'Piraí')
            ).order_by('nome')"""

        municipios = Municipio.objects.annotate(
            action_count=Count('action')
        ).order_by('action_count', 'nome')
        primeiro = municipios.first()
        municipios = municipios.filter(action_count=primeiro.action_count)
        print('tentativa', primeiro.action_count + 1,
              ': Total a fazer', municipios.count())

        urllib3.disable_warnings()
        http = urllib3.PoolManager(timeout=3.0)
        m_count = 0
        for m in municipios:
            m_count += 1
            if not m.domain:
                domainmask = '{}.{}.leg.br'

                nome = m.nome.replace(' ', '')

                domainmask = domainmask.format(
                    slugify(nome),
                    m.uf.lower()
                )

                m.domain = domainmask
                m.save()

            pesquisas = PesquisaNode.objects.filter(parent__isnull=True)

            def run(node, protocolo=None):

                if not isinstance(node, PesquisaNode):
                    for n in node:
                        run(n)
                    return

                if not protocolo:
                    errors = []
                    for p in node.protocolo:
                        try:
                            run(node, p)
                            errors = []
                            break
                        except Exception as e:
                            if hasattr(e, 'args'):
                                errors.append({p: e.args})
                            else:
                                errors.append({p: str(e)})
                            pass
                    if errors:
                        a = Action()
                        a.municipio = m
                        a.tipo = node
                        a.ping = False
                        a.json = errors
                        a.save()

                    if not node.restritivo or node.restritivo and not errors:
                        run(node.childs.all())
                    return

                uri = '{protocolo}://{servico}.{dominio}/{action}'.format(
                    protocolo=protocolo,
                    servico=node._servico,
                    dominio=m.domain,
                    action=node.action_view
                )

                print('GET:', m_count, uri, ' - ', m.nome,)
                data = None
                try:
                    r = http.request('GET', uri)

                    if not node.tipo_response:
                        a = Action()
                        a.municipio = m
                        a.tipo = node
                        a.ping = True
                        a.json = {
                            'status': r.status,
                            'reason': r.reason,
                            'uri': uri
                        }
                        a.save()
                        return

                except Exception as e:
                    print('...: erro..........................', str(e)[:50])
                    raise Exception(uri, str(e))

                try:
                    data = r.data.decode('utf-8')
                except Exception as e:
                    print('...: erro...')
                    raise Exception(uri, str(e))

                jdata = {}
                try:
                    jdata = json.loads(data)
                except Exception as e:
                    print('...: erro...')
                    raise Exception(uri, str(e))

                captures = node.tipo_response.split(',')

                funcs = {
                    'list': list,
                    'dict': dict
                }
                json_result = {}
                for capture in captures:
                    actions = capture.strip().split('__')

                    obj = jdata
                    for a in actions:
                        if a in funcs:
                            obj = funcs[a](obj)
                        else:
                            obj = obj[a]
                            json_result[a] = obj

                if not json_result:
                    json_result = {
                        'results': jdata
                    }

                json_result.update({
                    'status': r.status,
                    'reason': r.reason,
                    'uri': uri,
                })

                a = Action()
                a.municipio = m
                a.tipo = node
                a.ping = True
                a.json = json_result
                a.save()

            run(pesquisas)

            sleep(3)
