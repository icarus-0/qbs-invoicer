import django_filters
from django_filters import CharFilter
from .models import *

class client_filter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains')
    contact = CharFilter(field_name='contact',lookup_expr='icontains')
    address = CharFilter(field_name='address',lookup_expr='icontains')
    email = CharFilter(field_name='email',lookup_expr='icontains')
    class Meta:
        model = Client
        fields = '__all__'


class item_filter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains')
    desc = CharFilter(field_name='desc',lookup_expr='icontains')
    price = CharFilter(field_name='price',lookup_expr='icontains')
    class Meta:
        model = Item
        fields = '__all__'


class invoice_filter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = ('id','client','sync_status')