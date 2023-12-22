from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta

from django.db.models import Sum, IntegerField
# Product class
class Product(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.id} | {self.name}"
    

class Format(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.id} | {self.name}"


# Product Type class
class ProductType(models.Model):
    STORAGE_TYPE = (
        ('Sanaladigan', 'Sanaladigan'),
        ('Sanalmaydigan', 'Sanalmaydigan'),
    )
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE, default='Sanaladigan')
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    price = models.FloatField()
    
    
    @property
    def total_storage_count(self):
        if self.storage_type == 'Sanaladigan':
            total_import = self.storage_set.filter(action_type='Kiritish').aggregate(total_import=Sum('storage_count'))['total_import'] or 0
            total_remove = self.storage_set.filter(action_type='Chiqarish').aggregate(total_remove=Sum('storage_count'))['total_remove'] or 0
            return total_import - total_remove
        return None
    
    @property
    def current_storage_count(self):
        total_outcome_count = sum(outcome.outcome_count for outcome in self.outcome_set.all())
        total_income_count = sum(income.income_count for income in Income.objects.filter(outcome__protype=self))

        total_storage_count = self.total_storage_count
        if total_storage_count is None:
            total_storage_count = 0

        return total_storage_count - (total_outcome_count - total_income_count)

    
    def __str__(self):
        return f"{self.name}"

class Storage(models.Model):
    ACTION_TYPE = (
        ('Kiritish', 'Kiritish'),
        ('Chiqarish', 'Chiqarish'),
    )
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE, default='Kiritish')
    protype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    storage_count = models.PositiveBigIntegerField()
    storage_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.protype.name} |  {self.storage_count} | {self.storage_date}"
    

   
    
# Client class
class Client(models.Model):
    name = models.CharField(max_length=200)
    passport = models.CharField(max_length=13, null=True, blank=True)
    phone = models.CharField(max_length=13)
    desc = models.TextField(null=True, blank=True)
    
    @property
    def tranzactions(self):
        outcomes = Outcome.objects.filter(client=self).order_by('-id')
        incomes = Income.objects.filter(outcome__client=self).order_by('-id')
        payments = Payments.objects.filter(client=self).order_by('-id')
        additional_services = Addition_service.objects.filter(client=self)

        outcome_data = []
        income_data = []
        payments_data = []

        for outcome in outcomes:
            total_income_count = incomes.filter(outcome=outcome).aggregate(total=Sum('income_count'))['total'] or 0
            difference = outcome.outcome_count - total_income_count
            outcome_date = outcome.outcome_date.astimezone(timezone.get_current_timezone())

            total_incomes_summa = sum(income.income_summa for income in incomes)
            today = datetime.now(outcome.outcome_date.tzinfo)
            days_difference = (today - outcome.outcome_date).days
            daily_debt = (outcome.total_daily_price - total_incomes_summa) * days_difference if days_difference > 0 else 0

            protype_data = []
            for protype_instance in outcome.protype.all():
                protype_data.append({
                    "id": protype_instance.id,
                    "name": protype_instance.name,
                    "price": protype_instance.price,
                    "format": protype_instance.format.name
                })

            outcome_data.append({
                "id": outcome.id,
                "outcome_date": outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "protype": protype_data,
                "outcome_price_type": outcome.outcome_price_type,
                "outcome_count": outcome.outcome_count,
                "total_daily_price": outcome.total_daily_price,
                "outcome_price": outcome.outcome_price,
                "total_income_summa": total_incomes_summa,
                "income_count": total_income_count,
                "difference": difference,
                "daily_debt": daily_debt,
                "debt_days": days_difference,
            })

        for income in incomes:
            related_outcome = Outcome.objects.get(id=income.outcome_id)
            related_outcome_date = related_outcome.outcome_date.astimezone(timezone.get_current_timezone())

            outcome_info = {
                "id": related_outcome.id,
                "outcome_date": related_outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "protype": related_outcome.protype.name,
                "outcome_price_type": related_outcome.outcome_price_type,
                "outcome_count": related_outcome.outcome_count,
                "outcome_price": related_outcome.outcome_price,
                "total_daily_price": related_outcome.total_daily_price,
                "protype": {
                    "id": related_outcome.protype.id,
                    "name": related_outcome.protype.name,
                    "price": related_outcome.protype.price,
                    "format": related_outcome.protype.format.name
                }
            }

            income_date = income.income_date.astimezone(timezone.get_current_timezone())

            income_data.append({
                "id": income.id,
                "income_date": income_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "day": income.day,
                "income_count": income.income_count,
                "income_summa": income.income_summa,
                "outcome": outcome_info
            })

        for payment in payments:
            payments_data.append({
                "id": payment.id,
                "payment_summa": payment.payment_summa,
                "payment_date": payment.payment_date.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M:%S%z"),
                "desc": payment.desc,
            })

        total_payment = sum(payment.payment_summa for payment in payments)
        total_incomes_summa = sum(income.income_summa for income in incomes)
        debt = total_incomes_summa - total_payment
        total_service_price = sum(service.service_price for service in additional_services)

        return {
            "outcome_data": outcome_data,
            "income_data": income_data,
            "payments_data": payments_data,
            "total_payment": total_payment,
            "debt": debt,
            'total_incomes_summa': total_incomes_summa,
            "additional_services_data": list(additional_services.values()),  # Convert to list if necessary
            "total_service_price": total_service_price
        }

        
        

       
    @property
    def status(self):
        transactions = self.tranzactions
        if transactions['debt'] > 0 and any(outcome['difference'] > 0 for outcome in transactions['outcome_data']):
            return "Qarzdorlik"
        elif any(outcome['difference'] == 0 for outcome in transactions['outcome_data']):
            return "Aktiv"
        else:
            return "Shartnoma yakunlangan"
    def __str__(self):
        return f"{self.name} | {self.status}"

class Outcome(models.Model):
    PRICE_TYPE_CHOICES = (
        ('Narxida', 'Narxida'),
        ('Chegirmada', 'Chegirmada'),
    )
    outcome_price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    
    protype = models.ForeignKey(ProductType,on_delete=models.CASCADE)
    count = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    outcome_date = models.DateTimeField()

    @property
    def total_daily_price(self):
        total_price = 0
        for product_type in self.protype.all():
            if product_type.price == self.outcome_price:
                total_price += product_type.price * self.outcome_count
            else:
                total_price += self.outcome_price * self.outcome_count
        return total_price
    
    # def formatted_outcomes_array(self):
    #     formatted_outcomes = []
    #     for product_type in self.protype.all():
    #         formatted_outcome = {
    #             "protype": {
    #                 "id": product_type.id,
    #                 # "name": product_type.name,
    #                 "protype_price": str(product_type.price),
    #                 "format": product_type.format
    #             },
    #             "outcome_count": str(self.outcome_count),
    #             "outcome_price": str(self.outcome_price),
    #             "outcome_date": (self.outcome_date),
    #         }
    #         formatted_outcomes.append(formatted_outcome)
    #     return formatted_outcomes
    

        
    @property
    def debt_days(self):
        today = datetime.now(self.outcome_date.tzinfo)
        days_difference = (today - self.outcome_date).days
        return days_difference

        
    def __str__(self):
        return f" {self.protype.name} - {self.count}"


class Income(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    income_count = models.PositiveBigIntegerField()
    day = models.IntegerField()
    income_date = models.DateTimeField()

    # @property
    # def income_summa(self):
    #     return self.outcome.outcome_price*self.day
    
    @property
    def total_income_summa(self):
        related_incomes = Income.objects.filter(outcome=self.outcome)
        total_sum = sum(income.income_summa for income in related_incomes)
        return total_sum
    
    @property
    def income_summa(self):
        if self.outcome.outcome_price_type == "Narxida":
            return self.outcome.price * self.day * self.income_count
        elif self.outcome.outcome_price_type == "Chegirmada":
            return self.outcome.price * self.day * self.income_count  # Change this to self.income.income_price if needed
        else:
            return 0  # Or handle other cases as needed

    
    def __str__(self):
        return f"{self.outcome.client.name} - {self.income_count}"


class Payments(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    payment_summa = models.FloatField()
    payment_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.name} | {self.payment_summa}"



class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"

class Addition_service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    service_price = models.PositiveBigIntegerField()
    service_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.service_type.name} - {self.service_price}"
    
