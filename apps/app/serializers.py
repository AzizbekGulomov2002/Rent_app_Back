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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_instance = instance.product
        if product_instance:
            representation['product'] = ProductSerializer(product_instance).data
        else:
            representation['product'] = None
        format_instance = instance.format
        if format_instance:
            representation['format'] = FormatSerializer(format_instance).data
        else:
            representation['format'] = None
        return representation

    


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "passport", "phone", "transactions", "desc", ]


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = [
            "id",
            "client",
            "product",
            "count",
            "price",
            "date",
            # "total",
            "check_id"
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name if instance.client else None
        representation['product'] = instance.product.name if instance.product else None
        return representation


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "client",
            "product",
            "count",
            "income_price",
            "day",
            "date",
            "total",
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name if instance.client else None
        representation['product'] = instance.product.name if instance.product else None
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
