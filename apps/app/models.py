from django.db import models
from django.db.models import Sum
from django.utils import timezone

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
        outcomes = Outcome.objects.filter(client=self)
        incomes = Income.objects.filter(outcome__client=self)
        outcome_data = []
        income_data = []
        for outcome in outcomes:
            total_income_count = incomes.filter(outcome=outcome).aggregate(total=Sum('income_count'))['total'] or 0
            difference = outcome.outcome_count - total_income_count
            outcome_date = outcome.outcome_date.astimezone(timezone.get_current_timezone())
            protype = {
                "id": outcome.protype.id,
                "name": outcome.protype.name,
                "price": outcome.protype.price,
                "format": outcome.protype.format.name
            }

            outcome_data.append({
                "id": outcome.id,
                "outcome_date": outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "protype": outcome.protype.name,
                "outcome_count": outcome.outcome_count,
                "outcome_price": outcome.outcome_price,
                "income_count": total_income_count,
                # "day": day,
                "difference": difference,
                "protype": protype,
            })

        for income in incomes:
            related_outcome = Outcome.objects.get(id=income.outcome_id)
            related_outcome_date = income.income_date.astimezone(timezone.get_current_timezone())
            outcome_info = {
                "id": related_outcome.id,
                "outcome_date": related_outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "protype": related_outcome.protype.name,
                "outcome_count": related_outcome.outcome_count,
                "outcome_price": related_outcome.outcome_price,
                "protype": {
                    "id": related_outcome.protype.id,
                    "name": related_outcome.protype.name,
                    "price": related_outcome.protype.price,
                    "format": related_outcome.protype.format.name
                }
            }

            income_data.append({
                "id": income.id,
                "income_date": related_outcome_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "day": income.day,
                # "protype": income.outcome.protype.name,
                "income_count": income.income_count,
                "outcome": outcome_info
            })

        return {
            "outcome_data": outcome_data,
            "income_data": income_data
        }
        
    

    def __str__(self):
        return f"{self.name}"

class Outcome(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    protype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    outcome_count = models.FloatField()
    outcome_price = models.PositiveBigIntegerField()
    outcome_date = models.DateTimeField()
    check_id = models.IntegerField(default=1000)
    
    @property
    def total(self):
        if self.protype.price == self.outcome_price:
            return self.protype.price * self.outcome_count
        else:
            return self.outcome_price * self.outcome_count
        
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



    def __str__(self):
        return f"{self.outcome.client.name} - {self.income_count}"


class Payments(models.Model):
    class PayType(models.TextChoices):
        MAXSUS = "Maxsus to'lov", "Maxsus to'lov"
        TOLIQ = "To'liq yopish", "To'liq yopish"

    pay_type = models.CharField(
        max_length=30, choices=PayType.choices, null=True, blank=True
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    summa = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.client.name} | {self.product.name} | {self.summa}"



# 2023-12-09T11:04:19+05:00
# 2023-12-09T11:04:19+0500