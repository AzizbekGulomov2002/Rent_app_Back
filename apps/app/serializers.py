from rest_framework import serializers
from .models import *

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ["id", "name",]
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]

class ProTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name", "product", "format", "price"]
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     product_instance = instance.product
    #     if product_instance:
    #         representation['product'] = ProductSerializer(product_instance).data
    #     else:
    #         representation['product'] = None
    #     format_instance = instance.format
    #     if format_instance:
    #         representation['format'] = FormatSerializer(format_instance).data
    #     else:
    #         representation['format'] = None
    #     return representation
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance=instance.product).data
        representation['format'] = FormatSerializer(instance=instance.format).data
        return representation

    


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "passport", "phone","tranzactions", "desc"]



class OutcomeSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    class Meta:
        model = Outcome
        fields = [
            "id",
            "client",
            "protype",
            "outcome_count",
            "price",
            "date",
            # "total_incomes",
            # "difference",
            "check_id"
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['protype'] = ProTypeSerializer(instance=instance.protype).data
        return representation


class IncomeSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    class Meta:
        model = Income
        fields = [
            "id",
            "outcome",
            "income_count",
            "day",
            "date",
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['outcome'] = OutcomeSerializer(instance=instance.outcome).data
        return representation



class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "pay_type", "client", "product", "summa", "date"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name if instance.client else None
        representation['product'] = instance.product.name if instance.product else None
        return representation
