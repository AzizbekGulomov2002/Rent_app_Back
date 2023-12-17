from django_filters import rest_framework as filters
from apps.app.models import *
from django.db.models import fields
from django.db.models import F, Q, Sum, ExpressionWrapper
import django_filters

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ["name"]
        
class StorageFilter(filters.FilterSet):
    class Meta:
        model = Storage
        fields = ["protype","storage_date"]

class FormatFilter(filters.FilterSet):
    class Meta:
        model = Format
        fields = ["name"]
        
class ProductTypeFilter(filters.FilterSet):
    class Meta:
        model = ProductType
        fields = ["name", "product", "format"]


class ClientFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    passport = django_filters.CharFilter(field_name='passport', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    class Meta:
        model = Client
        fields = ["name", "passport", "phone"]


class OutcomeFilter(filters.FilterSet):
    class Meta:
        model = Outcome
        fields = ["client","protype", "outcome_date"]


class IncomeFilter(filters.FilterSet):
    class Meta:
        model = Income
        fields = ["outcome", "income_date"]


class PaymentsFilter(filters.FilterSet):
    class Meta:
        model = Payments
        fields = ["client", "payment_date"]



# class ServiceTypeFilter(filters.FilterSet):
#     class Meta:
#         model = ServiceType
#         fields = ["name"]


# class Addition_serviceFilter(filters.FilterSet):
#     class Meta:
#         model = Addition_service
#         fields = ["service_type", "service_date"]
