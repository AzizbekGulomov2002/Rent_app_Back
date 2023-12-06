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
    def transactions(self):
        outcomes = Outcome.objects.filter(client=self)
        incomes = Income.objects.filter(client=self)
        outcome_data = []
        income_data = []
        # totals = {}

        # Process outcome transactions
        for outcome in outcomes:
            outcome_data.append(
                {
                    "id": outcome.id,
                    "client": {
                        "id": outcome.client.id,
                        "name": outcome.client.name,
                    },
                    "product": {
                        "id": outcome.product.id,
                        "name": outcome.product.name,
                        "price": outcome.product.price  # Productning narxini chiqarish
                    },
                    "count": outcome.count,
                    "price": outcome.price,
                    "date": outcome.date,
                }
            )

            # Update totals with counts for outcome products
            product_id = outcome.product.id
            product_name = outcome.product.name
            # if product_id not in totals:
            #     totals[product_id] = {"id": product_id, "name": product_name, "counts_outcome": 0, "counts_income": 0}
            # totals[product_id]["counts_outcome"] += outcome.count

        # Process income transactions
        for income in incomes:
            income_data.append(
                {
                    "id": income.id,
                    "client": {
                        "id": income.client.id,
                        "name": income.client.name,
                    },
                    "product": {
                        "id": income.product.id,
                        "name": income.product.name,
                        "price": income.product.price  # Productning narxini chiqarish
                    },
                    "count": income.count,
                    "date": income.date,
                    "total": income.total,
                }
            )

            # Update totals with counts for income products
            product_id = income.product.id
            product_name = income.product.name
            # if product_id not in totals:
            #     totals[product_id] = {"id": product_id, "name": product_name, "counts_outcome": 0, "counts_income": 0}
            # totals[product_id]["counts_income"] += income.count

        # Calculate the difference for each product
        # for product_id, product_data in totals.items():
        #     product_data["difference"] = product_data["counts_outcome"] - product_data["counts_income"]
        #     del product_data["counts_outcome"]
        #     del product_data["counts_income"]

        return {
            "outcomes": outcome_data,
            "incomes": income_data,
            # "totals": list(totals.values()),
        }

    def __str__(self):
        return f"{self.name}"

class Outcome(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    count = models.FloatField()
    price = models.PositiveBigIntegerField(null=True, blank=True)
    date = models.DateTimeField()
    check_id = models.IntegerField(default=1000)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created for the first time
            last_outcome = Outcome.objects.last()  # Get the last Outcome object
            if last_outcome:
                self.check_id = last_outcome.check_id + 1  # Increment check_id by 1 based on the last Outcome
            else:
                self.check_id = 1000  # If there are no existing Outcome objects, start with 1000
            
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.client.name}, {self.product.name} - {self.count}"


class Income(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField()
    income_price = models.PositiveBigIntegerField(null=True, blank=True)
    day = models.IntegerField()
    date = models.DateTimeField()


    @property
    def total(self):
        if self.income_price is not None and self.pay > 0:
            return self.income_price * self.count
        elif self.product.price is not None:
            return self.product.price * self.count
        else:
            return 0

    def __str__(self):
        return f"{self.client.name}, {self.product.name} - {self.count}"


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
