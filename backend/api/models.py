from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import URLField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _

# Create your models here.
UF = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PR', 'Paraná'),
    ('PB', 'Paraíba'),
    ('PA', 'Pará'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins'),
    ('EX', 'Exterior'),
]

YES_NO_CHOICES = [(True, _('Sim')), (False, _('Não'))]


class Municipio(models.Model): 

    REGIAO_CHOICES = (
        ('CO', 'Centro-Oeste'),
        ('NE', 'Nordeste'),
        ('NO', 'Norte'),
        ('SE', 'Sudeste'),  # TODO convert on migrate SD => SE
        ('SL', 'Sul'),
        ('EX', 'Exterior'),
    )

    nome = models.CharField(max_length=50, blank=True)
    uf = models.CharField(
        max_length=2, blank=True, choices=UF)
    regiao = models.CharField(
        max_length=2, blank=True, choices=REGIAO_CHOICES)

    domain = URLField(default='')

    class Meta:
        verbose_name = _('Município')
        verbose_name_plural = _('Municípios')

    def __str__(self):
        return _('%(nome)s - %(uf)s (%(regiao)s)') % {
            'nome': self.nome, 'uf': self.uf, 'regiao': self.regiao
        }


class CrawlerAction(models.Model):
    municipio = ForeignKey(Municipio, on_delete=PROTECT)
        
    date_test = models.DateTimeField(
        verbose_name=_('Data de Teste'),
        editable=False, auto_now_add=True)

    ping_success = models.BooleanField(
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Sapl Respondeu'))
    
    json_casalegislativa = JSONField(default=dict)
        
    domain = URLField(default='')
    
