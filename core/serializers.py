from rest_framework import serializers
from .models import InvestmentFund, Transaction


class InvestmentFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentFund
        fields = ["id", "name", "ticker", "fund_type", "unit_price"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "date", "transaction_type", "value", "quantity", "fund"]
