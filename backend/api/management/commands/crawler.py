import json
from time import sleep

from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count
from django.utils.text import slugify
import urllib3
from backend.api.models import Municipio, CrawlerAction


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
            crawler_count=Count('crawleraction')
        ).order_by('crawler_count', 'nome')
        
        primeiro = municipios.first()
        
        municipios = municipios.filter(crawler_count=primeiro.crawler_count)
        
        print('tentativa', primeiro.crawler_count + 1, ': Fazendo 1000 de', municipios.count())
        
        urllib3.disable_warnings()
        http = urllib3.PoolManager(timeout=3.0)
        for m in municipios[:1000]:
            domain = m.domain
            if not domain:
                domainmask = '{}://{}.{}.{}.leg.br'
                
                nome = m.nome.replace(' ', '')
                
                domain = domainmask.format(
                    'https',
                    'sapl',
                    slugify(nome),
                    m.uf.lower()
                    )
               
                m.domain = domain
                m.save()
            
            c = CrawlerAction()
            c.municipio = m
            c.domain = domain 
            
            # print('test:', domain, ' - ', m.nome)
            try:                
                print('GET:', domain, ' - ', m.nome,)
                r = http.request('GET', ('{}/api/base/casalegislativa'.format(domain)))
                data = r.data.decode('utf-8')
                jdata = json.loads(data)
                c.json_casalegislativa = jdata['results']
                c.ping_success = True
            except Exception as e:
                c.json_casalegislativa = [{'error': str(e)}]
                
                print('.... ERROR:', domain, ' - ', m.nome)
                
            c.save()
            sleep(3)
