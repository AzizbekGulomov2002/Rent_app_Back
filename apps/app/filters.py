from django_filters import rest_framework as filters
from apps.app.models import *
from django.db.models import fields
from django.db.models import F, Q, Sum, ExpressionWrapper


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ["name"]

class FormatFilter(filters.FilterSet):
    class Meta:
        model = Format
        fields = ["name"]
        
class ProductTypeFilter(filters.FilterSet):
    class Meta:
        model = ProductType
        fields = ["name", "product", "format"]


class ClientFilter(filters.FilterSet):
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
        fields = ["pay_type", "product", "date"]
