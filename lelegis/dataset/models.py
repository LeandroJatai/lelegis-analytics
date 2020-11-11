from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import URLField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _


# Create your models here.
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
    #('EX', 'Exterior'),
]

YES_NO_CHOICES = [(True, _('Sim')), (False, _('Não'))]


class Municipio(models.Model):

    REGIAO_CHOICES = (
        ('CO', 'Centro-Oeste'),
        ('NE', 'Nordeste'),
        ('NO', 'Norte'),
        ('SE', 'Sudeste'),  # TODO convert on migrate SD => SE
        ('SL', 'Sul'),
        #('EX', 'Exterior'),
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


class PesquisaNode(models.Model):

    class Meta:
        verbose_name = _('Configuração de Pequisa')
        verbose_name_plural = _('Configurações de Pequisa')
        ordering = ('title', )

    title = models.CharField(max_length=1000,
                             blank=True, default='')

    parent = models.ForeignKey(
        'self',
        blank=True, null=True, default=None,
        related_name='childs',
        verbose_name=_('Parent'),
        on_delete=PROTECT)

    servico = models.CharField(max_length=30, default='', blank=True)

    action_view = models.CharField(max_length=1000,
                                   blank=True, default='')

    protocolos = models.CharField(max_length=30, default='https, http')

    restritivo = models.BooleanField(
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Restrige aprofundamento da árvore em caso de erro'))

    tipo_response = models.CharField(max_length=1000, default='', blank=True)
    description = models.TextField(blank=True, default='')

    @property
    def _servico(self):
        return self.servico if self.servico else self.parent._servico

    def __str__(self):
        str_self = '{}:{}'.format(self._servico, self.action_view)
        if not self.parent:
            return str_self
        return '{} - {}'.format(self.parent, str_self)


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
