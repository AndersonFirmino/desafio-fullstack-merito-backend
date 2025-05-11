import pytest
import json
from decimal import Decimal
import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import InvestmentFund, Transaction


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def investment_fund():
    return InvestmentFund.objects.create(
        name="Fundo de Teste",
        ticker="TEST11",
        fund_type="FII",
        unit_price=Decimal("75.50"),
    )


@pytest.mark.django_db
class TestInvestmentFundViews:
    def test_list_investment_funds(self, api_client, investment_fund):
        url = reverse("investmentfund-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == investment_fund.name
        assert response.data[0]["ticker"] == investment_fund.ticker

    def test_create_investment_fund(self, api_client):
        url = reverse("investmentfund-list")
        fund_data = {
            "name": "Novo Fundo",
            "ticker": "NOVO11",
            "fund_type": "FII",
            "unit_price": "120.75",
        }

        response = api_client.post(
            url,
            data=json.dumps(fund_data),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert InvestmentFund.objects.count() == 1

        fund = InvestmentFund.objects.first()
        assert fund.name == "Novo Fundo"
        assert fund.ticker == "NOVO11"
        assert fund.unit_price == Decimal("120.75")


@pytest.mark.django_db
class TestTransactionViews:
    def test_list_transactions(self, api_client, investment_fund):
        _ = Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="aporte",
            value=Decimal("500.00"),
            quantity=Decimal("6.6225"),
            fund=investment_fund,
        )

        url = reverse("transaction-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["transaction_type"] == "aporte"
        assert response.data[0]["value"] == "500.00"

    def test_create_transaction(self, api_client, investment_fund):
        url = reverse("transaction-list")
        transaction_data = {
            "date": datetime.date.today().isoformat(),
            "transaction_type": "resgate",
            "value": "300.00",
            "quantity": "3.9735",
            "fund": investment_fund.id,
        }

        response = api_client.post(
            url,
            data=json.dumps(transaction_data),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.count() == 1

        transaction = Transaction.objects.first()
        assert transaction.transaction_type == "resgate"
        assert transaction.value == Decimal("300.00")
        assert transaction.fund == investment_fund
