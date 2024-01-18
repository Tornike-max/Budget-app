from django.contrib import admin
from .models import FinancialEntry, ExpenseEntry

admin.site.register(FinancialEntry)
admin.site.register(ExpenseEntry)