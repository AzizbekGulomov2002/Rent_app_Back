from django.contrib import admin
from .models import (Product,ProductType,Client,Outcome,Income,Payments,Format,ServiceType,Addition_service)
admin.site.register(ProductType)


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
    ]
    list_per_page = 10
    class Meta:
        model = Client
admin.site.register(Client, ClientAdmin)


class FormatAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    list_per_page = 10
    class Meta:
        model = Format
admin.site.register(Format, FormatAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 10
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)


class OutcomeInline(admin.TabularInline):
    model = Outcome
    fields = ["client", "product", "outcome_count", "date"]


admin.site.register(Outcome)


class IncomeInline(admin.TabularInline):
    model = Income
    fields = ["outcome","count", "day", "date"]
admin.site.register(Income)





class PaymentsAdmin(admin.ModelAdmin):
    list_display = ["client", "payment_summa", "payment_date"]
    list_per_page = 10

    class Meta:
        model = Payments
admin.site.register(Payments, PaymentsAdmin)



class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_per_page = 10
    class Meta:
        model = ServiceType
admin.site.register(ServiceType, ServiceTypeAdmin)



class Addition_serviceAdmin(admin.ModelAdmin):
    list_display = ["id", "service_type", "service_price","service_date"]
    list_per_page = 10

    class Meta:
        model = Addition_service
admin.site.register(Addition_service, Addition_serviceAdmin)