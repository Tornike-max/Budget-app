from django.utils import timezone
from django.db.models import Sum
from rest_framework import generics, permissions
from .models import FinancialEntry, ExpenseEntry,FinancialGoal
from .serializers import FinancialEntrySerializer, ExpenseEntrySerializer,FinancialGoalSerializer



# მოაქვს ინფორმაცია ცალკე ხარჯების და შემოსავლების გასული 1კვირის, 1თვის, 1წლის
class BaseEntryTotalView(generics.ListAPIView):
    serializer_class = None
    queryset = None

    def get_queryset(self):
        period = self.kwargs['period']
        today = timezone.now().date()

        if period == 'week':
            start_date = today - timezone.timedelta(days=today.weekday())
            end_date = start_date + timezone.timedelta(days=7)
        elif period == 'month':
            start_date = today.replace(day=1)
            end_date = (start_date + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            return self.queryset.none()

        queryset = self.queryset.filter(entry_date__range=(start_date, end_date)).aggregate(
            total_salary=Sum('salary'),
            total_business_income=Sum('business_income'),
            total_rent_income=Sum('rent_income'),
            total_remittances=Sum('remittances'),
            total_other_financial=Sum('other'),
            total_utilities=Sum('utilities'),
            total_groceries_shopping=Sum('groceries_shopping'),
            total_transportation=Sum('transportation'),
            total_cafe_restaurant=Sum('cafe_restaurant'),
            total_health=Sum('health'),
            total_other_expense=Sum('other'),
        )

        return [queryset]


# შემოსავალს აკლებს ხარჯებს და გამოაქვს გასული კვირის, თვის, წლის მიხედვით.
class FinancialExpenseSummaryView(generics.ListAPIView):
    serializer_class = FinancialEntrySerializer

    def get_queryset(self):
        period = self.kwargs['period']

        financial_entries = FinancialEntry.objects.filter(entry_date__range=self.get_date_range(period))

        expense_entries = ExpenseEntry.objects.filter(entry_date__range=self.get_date_range(period))

        net_balance = self.calculate_net_balance(financial_entries, expense_entries)

        net_balance_entry = FinancialEntry(
            salary=net_balance['salary'],
            business_income=net_balance['business_income'],
            rent_income=net_balance['rent_income'],
            remittances=net_balance['remittances'],
            other=net_balance['other']
        )

        result_entries = list(financial_entries) + [net_balance_entry]

        return result_entries

    def calculate_net_balance(self, financial_entries, expense_entries):
        total_finances = {
            'salary': financial_entries.aggregate(total_salary=Sum('salary'))['total_salary'] or 0,
            'business_income': financial_entries.aggregate(total_business_income=Sum('business_income'))[
                'total_business_income'] or 0,
            'rent_income': financial_entries.aggregate(total_rent_income=Sum('rent_income'))['total_rent_income'] or 0,
            'remittances': financial_entries.aggregate(total_remittances=Sum('remittances'))['total_remittances'] or 0,
            'other': financial_entries.aggregate(total_other=Sum('other'))['total_other'] or 0,
        }

        total_expenses = {
            'utilities': -expense_entries.aggregate(total_utilities=Sum('utilities'))['total_utilities'] or 0,
            'groceries_shopping': -expense_entries.aggregate(total_groceries_shopping=Sum('groceries_shopping'))[
                'total_groceries_shopping'] or 0,
            'transportation': -expense_entries.aggregate(total_transportation=Sum('transportation'))[
                'total_transportation'] or 0,
            'cafe_restaurant': -expense_entries.aggregate(total_cafe_restaurant=Sum('cafe_restaurant'))[
                'total_cafe_restaurant'] or 0,
            'health': -expense_entries.aggregate(total_health=Sum('health'))['total_health'] or 0,
            'other_expense': -expense_entries.aggregate(total_other_expense=Sum('other'))['total_other_expense'] or 0,
        }

        net_balance = {
            'salary': total_finances['salary'] + total_expenses['salary'],
            'business_income': total_finances['business_income'] + total_expenses['business_income'],
            'rent_income': total_finances['rent_income'] + total_expenses['rent_income'],
            'remittances': total_finances['remittances'] + total_expenses['remittances'],
            'other': total_finances['other'] + total_expenses['other'],
        }

        return net_balance

    def get_date_range(self, period):
        today = timezone.now().date()

        if period == 'week':
            start_date = today - timezone.timedelta(days=today.weekday())
            end_date = start_date + timezone.timedelta(days=6)
        elif period == 'month':
            start_date = today.replace(day=1)
            end_date = (start_date + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            raise ValueError("Invalid period")

        return start_date, end_date


class FinancialEntryListCreateView(generics.ListCreateAPIView):
    queryset = FinancialEntry.objects.all()
    serializer_class = FinancialEntrySerializer


class FinancialEntryTotalView(BaseEntryTotalView):
    queryset = FinancialEntry.objects.all()
    serializer_class = FinancialEntrySerializer


class ExpenseEntryListCreateView(generics.ListCreateAPIView):
    queryset = ExpenseEntry.objects.all()
    serializer_class = ExpenseEntrySerializer


class ExpenseEntryTotalView(BaseEntryTotalView):
    queryset = ExpenseEntry.objects.all()
    serializer_class = ExpenseEntrySerializer


class FinancialEntryListCreateView(generics.ListCreateAPIView):
    queryset = FinancialEntry.objects.all()
    serializer_class = FinancialEntrySerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseEntryListCreateView(generics.ListCreateAPIView):
    queryset = ExpenseEntry.objects.all()
    serializer_class = ExpenseEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

class FinancialGoalListCreateView(generics.ListCreateAPIView):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinancialGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)