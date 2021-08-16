from django.db.models import fields
import django_filters
from django_filters import DateFilter
from .models import Client


class LoanFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='loan_drawn_date',lookup_expr='gte')
    end_date = DateFilter(field_name='loan_drawn_date',lookup_expr='lte')
    class Meta:
        model = Client
        fields = ['name','amount']
