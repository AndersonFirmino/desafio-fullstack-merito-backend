from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Case, When, DecimalField, F
from rest_framework.reverse import reverse
from .models import InvestmentFund, Transaction
from .serializers import InvestmentFundSerializer, TransactionSerializer

# Views will be added here


class APIRootView(APIView):
    """
    API root view that returns all available endpoints.
    """

    def get(self, request, format=None):
        return Response(
            {
                "investment-funds": reverse(
                    "investmentfund-list", request=request, format=format
                ),
                "transactions": reverse(
                    "transaction-list", request=request, format=format
                ),
                "wallet-summary": reverse(
                    "wallet-summary", request=request, format=format
                ),
            }
        )


class InvestmentFundViewSet(viewsets.ModelViewSet):
    queryset = InvestmentFund.objects.all()
    serializer_class = InvestmentFundSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletSummaryView(APIView):
    def get(self, request):
        funds_with_transactions = InvestmentFund.objects.filter(
            transactions__isnull=False
        ).distinct()

        wallet_summary = {"total_balance": 0, "funds": []}

        for fund in funds_with_transactions:
            net_quantity = (
                Transaction.objects.filter(fund=fund).aggregate(
                    net_quantity=Sum(
                        Case(
                            When(transaction_type="aporte", then=F("quantity")),
                            When(transaction_type="resgate", then=-F("quantity")),
                            default=0,
                            output_field=DecimalField(),
                        )
                    )
                )["net_quantity"]
                or 0
            )

            current_value = net_quantity * fund.unit_price

            wallet_summary["total_balance"] += current_value

            wallet_summary["funds"].append(
                {
                    "id": fund.id,
                    "name": fund.name,
                    "ticker": fund.ticker,
                    "total_quantity": net_quantity,
                    "unit_price": fund.unit_price,
                    "estimated_value": current_value,
                }
            )

        return Response(wallet_summary)
