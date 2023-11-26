from rest_framework import serializers
from .models import *

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ["id", "name",]

class ProTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name", "product", "format", "price"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.name if instance.product else None
        representation['format'] = instance.format.name if instance.format else None
        return representation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "passport", "phone", "desc", "transactions"]


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = [
            "id",
            "client",
            "client_name",
            "product",
            "product_name",
            "count",
            "price",
            "date",
            "total",
            "check_id"
        ]
        # depth=1


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "client",
            "client_name",
            "product",
            "product_name",
            "count",
            "income_price",
            "day",
            "date",
            "total",
        ]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "pay_type", "client", "product", "summa", "date"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name if instance.client else None
        representation['product'] = instance.product.name if instance.product else None
        return representation
