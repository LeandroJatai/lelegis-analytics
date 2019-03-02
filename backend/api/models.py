from django import forms
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import URLField, SlugField
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import SelectMultiple
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

    domain = models.CharField(max_length=1000, default='')
    
    class Meta:
        verbose_name = _('Município')
        verbose_name_plural = _('Municípios')

    def __str__(self):
        return _('%(nome)s - %(uf)s (%(regiao)s)') % {
            'nome': self.nome, 'uf': self.uf, 'regiao': self.regiao
        }


class ArraySelectMultiple(SelectMultiple):

    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
            'widget': ArraySelectMultiple,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        res = super().to_python(value)
        if isinstance(res, list):
            value = [self.base_field.to_python(val) for val in res]
        return value


class PesquisaNode(models.Model):
    
    PROTOCOLO_CHOICES = (
        ('https', 'https'),
        ('http', 'http'),
        ('wss', 'wss'),
        ('ws', 'ws'),
    )    
    
    parent = models.ForeignKey(
        'self',
        blank=True, null=True, default=None,
        related_name='childs',
        verbose_name=_('Parent'),
        on_delete=PROTECT)
    
    servico = models.CharField(max_length=30, default='', blank=True) 

    action_view = models.CharField(max_length=1000,
        blank=True, default='') 

    protocolo = ChoiceArrayField(
        models.CharField(max_length=10,
                         choices=PROTOCOLO_CHOICES),
        default=list)
        
    restritivo = models.BooleanField(
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Restrige aprofundamento da árvore'))
    
    tipo_response = models.CharField(max_length=1000, default='', blank=True) 
    
    @property
    def _servico(self):
        return self.servico if self.servico else self.parent._servico
    
    def __str__(self):
        str_self = '{}:{}'.format(self._servico, self.action_view)
        if not self.parent:
            return str_self
        return '{} - {}'.format(self.parent, str_self)


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


class Action(models.Model):
    municipio = ForeignKey(Municipio, on_delete=PROTECT)
    
    tipo = models.ForeignKey(
        PesquisaNode, on_delete=PROTECT)
        
    data = models.DateTimeField(
        verbose_name=_('Data de Teste'),
        editable=False, auto_now_add=True)

    ping = models.BooleanField(
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Serviço Respondeu'))
    
    json = JSONField(default=dict)
        
    domain = URLField(default='')
    
