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
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


# Pagination class

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


# Product Type class
    

class ProTypeViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductType.objects.all()
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter
    search_fields = ('name',)
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

# Products out of the paginations class
    
class AllProTypeViewset(ModelViewSet):
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductTypeFilter 
    search_fields = ['name', 'format']
    filterset_fields = ('price', 'name', 'format')
    ordering_fields = ('price', 'name', 'format')  
    ordering = ('price',)


# Formats for Products class

class FormatViewset(ModelViewSet):
    queryset = Format.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = FormatSerializer
    filterset_class = FormatFilter
    search_fields = ["name"]


# Products class
    
class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name"]


# Storage for Products class
    

class StorageViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StorageFilter
    search_fields = ["protype"]
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    

# Clients class
    
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

# Outcome Export class

# class OutcomeViewset(viewsets.ModelViewSet):
#     queryset = Outcome.objects.all().order_by("-id")
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ("client", "outcome_count", "outcome_price", "outcome_date")
#     filterset_class = OutcomeFilter
#     serializer_class = OutcomeSerializer


class OutcomeViewset(viewsets.ModelViewSet):
    queryset = Outcome.objects.all().order_by("-id")
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("client", "outcome_count", "outcome_price", "outcome_date")
    filterset_class = OutcomeFilter
    serializer_class = OutcomeSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OutcomeBulkCreateSerializer
        return OutcomeSerializer
    def create(self, request, *args, **kwargs):
        serializer = OutcomeBulkCreateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            client_id = validated_data.pop('client')
            protypes = validated_data.pop('protypes')
            outcome_date = validated_data.pop('outcome_date')
            objects = []
            for protyp in protypes:
                objects.append(Outcome.objects.create(client_id=client_id, outcome_date=outcome_date, **protyp))
            protypes = OutcomeSerializer(objects, many=True)
            data = {"client": client_id, "outcome_date": outcome_date, "protypes": protypes.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Income Import class

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



# Payments class

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


#  Service Types class

class ServiceTypeViewset(ModelViewSet):
    queryset = ServiceType.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = ServiceTypeSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


# Addition services class
    

class Addition_serviceViewset(CustomPaginationMixin, viewsets.ModelViewSet):
    queryset = Addition_service.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = Addition_serviceSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
