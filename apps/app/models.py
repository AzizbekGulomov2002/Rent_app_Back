from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
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
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    price = models.FloatField()
    storage_count = models.PositiveBigIntegerField()
    
    @property
    def difference_storage_count(self):
        total_outcome_count = Outcome.objects.filter(protype=self).aggregate(total=Sum('outcome_count'))['total'] or 0
        total_income_count = Income.objects.filter(outcome__protype=self).aggregate(total=Sum('income_count'))['total'] or 0

        return self.storage_count - total_outcome_count + total_income_count
    def __str__(self):
        return f"{self.name}"
    
    
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
        outcome_data = []
        income_data = []
        payments_data = []
        
        for outcome in outcomes:
            # Loop through Outcome objects
            total_income_count = incomes.filter(outcome=outcome).aggregate(total=Sum('income_count'))['total'] or 0
            difference = outcome.outcome_count - total_income_count
            outcome_date = outcome.outcome_date.astimezone(timezone.get_current_timezone())

            protype = {
                "id": outcome.protype.id,
                "name": outcome.protype.name,
                "price": outcome.protype.price,
                "format": outcome.protype.format.name
            }
            related_incomes = Income.objects.filter(outcome=outcome)
            total_income_summa = sum(income.income_summa for income in related_incomes)

            

            # Calculate daily_debt and debt_days here
            daily_debt = 0  # Replace with your calculation for daily_debt
            debt_days = 0  # Replace with your calculation for debt_days

            outcome_data.append({
                "id": outcome.id,
                "outcome_date": outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "protype": outcome.protype.name,
                "outcome_price_type": outcome.outcome_price_type,
                "outcome_count": outcome.outcome_count,
                "total_daily_price": outcome.total_daily_price,
                "outcome_price": outcome.outcome_price,
                "total_income_summa": total_income_summa,
                "income_count": total_income_count,
                "difference": difference,
                "protype": protype,
                "daily_debt": daily_debt,  # Include daily_debt here
                "debt_days": debt_days,  # Include debt_days here
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
            # Loop through Payment objects
            payments_data.append({
                "id": payment.id,
                "payment_summa": payment.payment_summa,
                "payment_date": payment.payment_date.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M:%S%z"),
                "desc": payment.desc,
            })
        # total_income_summa = sum(income.income_summa for income in incomes)  
        total_income_summa = sum(map(lambda x: x.income_summa, incomes))    
        total_payment = sum(payment.payment_summa for payment in payments)
        # total_incomes_summa = sum(total_income_summa for income in incomes) # all of total_income_summa sums
        total_incomes_summa = sum(map(lambda x: x.income_summa, incomes))
        debt = total_incomes_summa - total_payment
        
        additional_services_data = []
        additional_services = Addition_service.objects.filter(client=self)
        total_service_price = sum(service.service_price for service in additional_services)
        for service in additional_services:
            service_type = {
                "id": service.service_type.id,
                "name": service.service_type.name
                # Other fields you want to include
            }
            additional_services_data.append({
                "id": service.id,
                "service_type": service_type,
                "service_price": service.service_price,
                "service_date": service.service_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "desc": service.desc
                # Other fields you want to include
            })

        return {
            "outcome_data": outcome_data,
            "income_data": income_data,
            "payments_data": payments_data,
            "total_payment": total_payment,
            "debt": debt,
            'total_incomes_summa':total_incomes_summa,
            "additional_services_data": additional_services_data,
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
    protype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    outcome_count = models.FloatField()
    outcome_price = models.PositiveBigIntegerField()
    outcome_date = models.DateTimeField()
    check_id = models.IntegerField(default=1000)
    
    @property
    def total_daily_price(self):
        if self.protype.price == self.outcome_price:
            return self.protype.price * self.outcome_count
        else:
            return self.outcome_price * self.outcome_count

    # @property
    # def daily_debt(self):
    #     transactions = self.tranzactions
    #     outcomes_data = transactions['outcome_data']
    #     for outcome in outcomes_data:
    #         if outcome['difference'] > 0:
    #             outcome_date = datetime.strptime(outcome['outcome_date'], "%Y-%m-%dT%H:%M:%S%z")
    #             today = datetime.now(outcome_date.tzinfo)
    #             days_difference = (today - outcome_date).days
    #             daily_debt = days_difference * outcome['protype']['price']  # Replace 'price' with your actual field
    #             return daily_debt
    #     return 0
    

        
    @property
    def debt_days(self):
        today = datetime.now(self.outcome_date.tzinfo)
        days_difference = (today - self.outcome_date).days
        return days_difference if days_difference > 0 and self.difference > 0 else 0
        
    
        
    def save(self, *args, **kwargs):
        if not self.pk:
            last_outcome = Outcome.objects.last()
            if last_outcome:
                self.check_id = last_outcome.check_id + 1
            else:
                self.check_id = 1000 
        super().save(*args, **kwargs)
    
    
    

    
    
    def __str__(self):
        return f"{self.client.name}, {self.protype.name} - {self.outcome_count}"


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
            return self.outcome.outcome_price * self.day * self.income_count
        elif self.outcome.outcome_price_type == "Chegirmada":
            return self.outcome.outcome_price * self.day * self.income_count  # Change this to self.income.income_price if needed
        else:
            return 0  # Or handle other cases as needed

    # @property
    # def debt_days(self):
    #     today = datetime.now(timezone.now().tzinfo)
    #     days_difference = (today - self.income_date).days
    #     return days_difference if days_difference > 0 and self.outcome.difference > 0 else 0
    
    def __str__(self):
        return f"{self.outcome.client.name} - {self.income_count}"


class Payments(models.Model):
    # class PayType(models.TextChoices):
    #     MAXSUS = "Maxsus to'lov", "Maxsus to'lov"
    #     TOLIQ = "To'liq yopish", "To'liq yopish"

    # pay_type = models.CharField(
    #     max_length=30, choices=PayType.choices, null=True, blank=True
    # )
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
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    service_price = models.PositiveBigIntegerField()
    service_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.service_type.name} - {self.service_price}"
    
