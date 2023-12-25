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


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "protype","action_type", "storage_count", "storage_date","desc"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['protype'] = ProTypeSerializer(instance=instance.protype).data
        return representation


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "passport", "phone","tranzactions", "desc","status"]
        

class OutcomePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = [
            "protype",
            "outcome_price_type",
            "outcome_count",
            "outcome_price",
        ]
class OutcomeBulkCreateSerializer(serializers.Serializer):
    client = serializers.IntegerField(required=True, write_only=True)
    outcome_date = serializers.DateTimeField(required=True)
    protypes = OutcomePostSerializer(many=True, write_only=True)


class OutcomeSerializer(serializers.ModelSerializer):
    outcome_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    income_count = serializers.SerializerMethodField()
    difference = serializers.SerializerMethodField() 
    class Meta:
        model = Outcome
        fields = [
            "id",
            "client",
            "protype",  
            "outcome_price_type",     
            "outcome_count",
            "outcome_price",  
            "outcome_date",
            "income_count",
            "difference",
            "total_daily_price",
        ]
    def get_protype_representation(self, protype_instance):
        return {
            "id": protype_instance.id,
            "protype_price": protype_instance.price,
        }
    def get_income_count(self, instance):
        incomes = Income.objects.filter(outcome=instance)
        total_income_count = incomes.aggregate(total=Sum('income_count'))['total'] or 0
        return total_income_count

    def get_difference(self, instance):
        incomes = Income.objects.filter(outcome=instance)
        total_income_count = incomes.aggregate(total=Sum('income_count'))['total'] or 0
        instance_count = int(instance.outcome_count) if instance.outcome_count else 0
        return instance_count - total_income_count




class ProTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id","name","storage_type", "product", "format", "price","total_storage_count","current_storage_count"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance=instance.product).data
        representation['format'] = FormatSerializer(instance=instance.format).data
        return representation


class IncomeSerializer(serializers.ModelSerializer):
    income_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    class Meta:
        model = Income
        fields = [
            "id",
            "outcome",
            "income_count",
            "day",
            "income_date",
            "income_summa",
            "total_income_summa"
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['outcome'] = OutcomeSerializer(instance=instance.outcome).data
        return representation



class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ["id", "client","payment_summa", "payment_date","desc"]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name if instance.client else None
        return representation


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name"]


class Addition_serviceSerializer(serializers.ModelSerializer):
    # service_type = ServiceTypeSerializer() 
    class Meta:
        model = Addition_service
        fields = ["id","client", "service_type", "service_price", "service_date", "desc"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['service_type'] = ServiceTypeSerializer(instance=instance.service_type).data
        return representation

