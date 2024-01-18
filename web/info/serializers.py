from rest_framework import serializers
from .models import FinancialEntry, ExpenseEntry

class FinancialEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialEntry
        fields = '__all__'

class ExpenseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = '__all__'

    # def create(self, validated_data):
    #     self.utilities = -abs(self.utilities) if self.utilities is not None else None
    #     utilities = validated_data.pop('utilities', 0)