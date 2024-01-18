from django.urls import path
from .views import FinancialEntryListCreateView, FinancialEntryTotalView, ExpenseEntryListCreateView, \
    ExpenseEntryTotalView, FinancialExpenseSummaryView

urlpatterns = [
    path('financial-entries/', FinancialEntryListCreateView.as_view(), name='financial-entry-list-create'),
    path('financial-entries/total/<int:period>/', FinancialEntryTotalView.as_view(), name='financial-entry-total'),

    path('expense-entries/', ExpenseEntryListCreateView.as_view(), name='expense-entry-list-create'),
    path('expense-entries/total/<int:period>/', ExpenseEntryTotalView.as_view(), name='expense-entry-total'),

    path('financial-expense-summary/<int:period>/', FinancialExpenseSummaryView.as_view(), name='financial-expense-summary'),
]
