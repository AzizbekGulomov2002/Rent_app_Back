from django.db import models

# from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum


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

            outcome_data.append({
                "id": outcome.id,
                "date": outcome.date,
                "protype": outcome.protype.name,
                "total_outcome_count": outcome.outcome_count,
            })

        for income in incomes:
            related_outcome = Outcome.objects.get(id=income.outcome_id)
            outcome_info = {
                "id": related_outcome.id,
                "date": related_outcome.date,
                "protype": related_outcome.protype.name,
                "outcome_count": related_outcome.outcome_count,
            }

            income_data.append({
                "id": income.id,
                "date": income.date,
                "protype": income.outcome.protype.name,
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
    price = models.PositiveBigIntegerField()
    date = models.DateTimeField()
    check_id = models.IntegerField(default=1000)
    
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
    date = models.DateTimeField()



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
