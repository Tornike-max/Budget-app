from rest_framework import serializers
from .models import FinancialEntry, ExpenseEntry,FinancialGoal


class FinancialEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialEntry
        fields = '__all__'
        extra_kwargs = {
            'salary': {'allow_null': True},
            'business_income': {'allow_null': True},
            'rent_income': {'allow_null': True},
            'remittances': {'allow_null': True},
            'other': {'allow_null': True},
        }

class ExpenseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = '__all__'


class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = '__all__'

    # def create(self, validated_data):
    #     self.utilities = -abs(self.utilities) if self.utilities is not None else None
    #     utilities = validated_data.pop('utilities', 0)