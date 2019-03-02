from django.db.models.fields.files import FileField
from django.utils.text import capfirst
from django_filters.filters import CharFilter
from django_filters.rest_framework.filterset import FilterSet
from django_filters.utils import resolve_field
from api.models import Municipio


class FilterSetMixin(FilterSet):

    o = CharFilter(method='filter_o')

    class Meta:
        fields = '__all__'
        filter_overrides = {
            FileField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                },
            },
        }

    def filter_o(self, queryset, name, value):
        try:
            return queryset.order_by(
                *map(str.strip, value.split(',')))
        except:
            return queryset

    @classmethod
    def filter_for_field(cls, f, name, lookup_expr='exact'):
        # Redefine método estático para ignorar filtro para
        # fields que não possuam lookup_expr informado
        f, lookup_type = resolve_field(f, lookup_expr)

        default = {
            'field_name': name,
            'label': capfirst(f.verbose_name),
            'lookup_expr': lookup_expr
        }

        filter_class, params = cls.filter_for_lookup(
            f, lookup_type)
        default.update(params)
        if filter_class is not None:
            return filter_class(**default)
        return None

    
class MunicipioFilterSet(FilterSetMixin):

    class Meta(FilterSetMixin.Meta):
        model = Municipio
