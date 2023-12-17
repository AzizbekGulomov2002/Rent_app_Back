from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from apps.app.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50000

    def get_paginated_response(self, data):
        return Response({
            "page_size": self.page_size,
            "total_objects": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page_number": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
class CustomPaginationMixin:
    pagination_class = BasePagination

class ProTypeViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filterset_fields = ('price', 'name','format')
    queryset = ProductType.objects.all()
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter
    search_fields = ('name',)
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class AllProTypeViewset(ModelViewSet):
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter 
    search_fields = ['name', 'format']
    filterset_fields = ('price', 'name', 'format')
    ordering_fields = ('price', 'name', 'format')  # Specify fields for sorting/ordering
    ordering = ('price',)  # Initial default ordering



class FormatViewset(ModelViewSet):
    queryset = Format.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = FormatSerializer
    filterset_class = FormatFilter
    search_fields = ["name"]


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name"]


class StorageViewset(ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StorageFilter
    search_fields = ["protype"]


class ClientViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("name", "passport", "phone")
    # filterset_fields = ('status', )
    filterset_class = ClientFilter
    serializer_class = ClientSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class OutcomeViewset(ModelViewSet):
    queryset = Outcome.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("client","outcome_count", "outcome_price", "outcome_date")
    filterset_class = OutcomeFilter
    serializer_class = OutcomeSerializer



class IncomeViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("income_count","income_date")
    filterset_class = IncomeFilter
    serializer_class = IncomeSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PaymentsViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Payments.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("payment_date")
    # filterset_fields = ('status', )
    filterset_class = PaymentsFilter
    serializer_class = PaymentsSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ServiceTypeViewset(ModelViewSet):
    queryset = ServiceType.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields = ("payment_date")  
    # filterset_class = ServiceTypeFilter
    serializer_class = ServiceTypeSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class Addition_serviceViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Addition_service.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields = ("payment_date")
    # filterset_class = Addition_serviceFilter
    serializer_class = Addition_serviceSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
