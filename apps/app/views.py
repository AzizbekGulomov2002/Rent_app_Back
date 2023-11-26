from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet

from apps.app.filters import *
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework import pagination, response


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
    queryset = ProductType.objects.all().order_by("-id")
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter 
    search_fields = ['name','price'] 
    filterset_fields = {'name__related_field': ['icontains']}
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class AllProTypeViewset(ModelViewSet):
    queryset = ProductType.objects.all().order_by("-id")
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter 
    search_fields = ['name','price'] 
    filterset_fields = {'name__related_field': ['icontains']}



class FormatViewset(ModelViewSet):
    queryset = Format.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = FormatSerializer
    filterset_class = FormatFilter
    search_fields = ["name"]


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name"]



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


class OutcomeViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Outcome.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("count", "price", "date","check_id")
    filterset_class = OutcomeFilter
    serializer_class = OutcomeSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class IncomeViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("count", "price", "date")
    filterset_class = IncomeFilter
    serializer_class = IncomeSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PaymentsViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Payments.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("count", "price", "date")
    # filterset_fields = ('status', )
    filterset_class = PaymentsFilter
    serializer_class = PaymentsSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
