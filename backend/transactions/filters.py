import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    month = django_filters.CharFilter(method='filter_by_month')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['category', 'transaction_type', 'month', 'start_date', 'end_date']

    def filter_by_month(self, queryset, name, value):
        try:
            year, month = value.split('-')
            return queryset.filter(date__year=int(year), date__month=int(month))
        except (ValueError, AttributeError):
            return queryset
