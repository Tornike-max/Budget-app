from django.db import models
from myapp.models import CustomUser
from django.conf import settings

class FinancialEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    business_income = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    rent_income = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    remittances = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    other = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry {self.id} - {self.entry_date}"

class ExpenseEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    utilities = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    groceries_shopping = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    transportation = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    cafe_restaurant = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    health = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    other = models.DecimalField(max_digits=10000000000, decimal_places=2, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense Entry {self.id} - {self.entry_date}"

    def save(self, *args, **kwargs):
        self.utilities = -abs(self.utilities) if self.utilities is not None else None
        self.groceries_shopping = -abs(self.groceries_shopping) if self.groceries_shopping is not None else None
        self.transportation = -abs(self.transportation) if self.transportation is not None else None
        self.cafe_restaurant = -abs(self.cafe_restaurant) if self.cafe_restaurant is not None else None
        self.health = -abs(self.health) if self.health is not None else None
        self.other = -abs(self.other) if self.other is not None else None

        super().save(*args, **kwargs)
