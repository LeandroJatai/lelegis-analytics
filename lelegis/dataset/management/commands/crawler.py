import json
import logging
import socket
from time import sleep

from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count, Max
from django.utils.text import slugify
import urllib3
from urllib3.util.timeout import Timeout

from lelegis.dataset.models import Municipio, PesquisaNode, Action


class Command(BaseCommand):
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('action', nargs='?', type=str, default='new')
        parser.add_argument('limit', nargs='?', type=str, default=0)

        # action
        # all, new, update_ping_true, update_ping_false

        # all - executa todos os nós de pesquisa

        # new - executa nós que nunca foram executados

        # update_ping_true - reexecuta os actions já existentes com ping true
        # update_ping_false - reexecuta os actions já existentes com ping false

        # default: new

    def handle(self, *args, **options):

        action = options['action']
        limit = options['limit']

        """
        municipios = Municipio.objects.filter(
            nome__in=(
                'Jataí',
                'Formosa',
                'Ibiúna',
                'Agudo',
                'Piraí')
        ).order_by('nome')
        """

        municipios = Municipio.objects.annotate(
            data_last_action=Max('action__data')
        ).order_by('data_last_action')

        if limit:
            municipios = municipios[:limit]

        urllib3.disable_warnings()

        timeout = Timeout(connect=5.0, read=10.0)
        http = urllib3.PoolManager(timeout=timeout)

        for m in municipios:
            print('....TEST:', m)

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

                try:
                    a = Action.objects.get(municipio=m, tipo=node)
                except:
                    a = Action()

                if a.id:
                    if action == 'new':

                        if not a.ping and node.restritivo:
                            return

                        run(node.childs.all())
                        return

                    elif action == 'update_ping_false':

                        if a.ping:
                            run(node.childs.all())
                            return

                    elif action == 'update_ping_true':

                        if not a.ping and not node.restritivo:
                            run(node.childs.all())
                            return

                else:
                    if action.startswith('update_ping'):
                        return

                if not protocolo:
                    errors = []
                    for p in node.protocolos.split(','):
                        try:
                            run(node, p.strip())
                            errors = []
                            break
                        except Exception as e:
                            if hasattr(e, 'args'):
                                errors.append({p: e.args})
                            else:
                                errors.append({p: str(e)})
                            pass
                    if errors:
                        a.municipio = m
                        a.tipo = node
                        a.ping = False
                        a.json = errors
                        a.save()

                    if not node.restritivo or node.restritivo and not errors:
                        run(node.childs.all())
                    return

                print('GET:', m, node)

                # return - exec fake
                # print('exec fake')
                # return

                uri = '{protocolo}://{servico}.{dominio}/{action}'.format(
                    protocolo=protocolo,
                    servico=node._servico,
                    dominio=m.domain,
                    action=node.action_view
                )

                data = None

                try:
                    r = http.request('GET', uri)

                    if not node.tipo_response:
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
                    for f in actions:
                        if f in funcs:
                            obj = funcs[f](obj)
                        else:
                            obj = obj[f]
                            json_result[f] = obj

                if not json_result:
                    json_result = {
                        'results': jdata
                    }

                json_result.update({
                    'status': r.status,
                    'reason': r.reason,
                    'uri': uri,
                })

                a.municipio = m
                a.tipo = node
                a.ping = True
                a.json = json_result
                a.save()

                sleep(1)

            run(pesquisas)

    def ping(self, url):
        try:
            socket.setdefaulttimeout(5)
            host = socket.gethostbyname(url.split('//')[1].split('/')[0])
            s = socket.create_connection(
                (host, 443 if 'https' in url else 80), 2)
            s.close()
            return True

        except Exception as e:
            self.logger.error('Ping Error:', url, e)
            return False
