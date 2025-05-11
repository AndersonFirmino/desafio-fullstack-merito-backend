import pytest
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
def investment_fund_1():
    return InvestmentFund.objects.create(
        name="Fundo de Teste 1",
        ticker="TEST1",
        fund_type="FII",
        unit_price=Decimal("100.00"),
    )


@pytest.fixture
def investment_fund_2():
    return InvestmentFund.objects.create(
        name="Fundo de Teste 2",
        ticker="TEST2",
        fund_type="FII",
        unit_price=Decimal("50.00"),
    )


@pytest.mark.django_db
class TestWalletSummaryView:
    def test_basic_wallet_with_one_fund(self, api_client, investment_fund_1):
        Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="aporte",
            value=Decimal("500.00"),
            quantity=Decimal("5.0"),
            fund=investment_fund_1,
        )

        Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="resgate",
            value=Decimal("200.00"),
            quantity=Decimal("2.0"),
            fund=investment_fund_1,
        )

        url = reverse("wallet-summary")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["total_balance"]) == Decimal("300.00")
        assert len(response.data["funds"]) == 1

        fund_data = response.data["funds"][0]
        assert fund_data["name"] == "Fundo de Teste 1"
        assert fund_data["ticker"] == "TEST1"
        assert Decimal(fund_data["total_quantity"]) == Decimal("3.0")
        assert Decimal(fund_data["unit_price"]) == Decimal("100.00")
        assert Decimal(fund_data["estimated_value"]) == Decimal("300.00")

    def test_multiple_funds_wallet(
        self, api_client, investment_fund_1, investment_fund_2
    ):
        Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="aporte",
            value=Decimal("1000.00"),
            quantity=Decimal("10.0"),
            fund=investment_fund_1,
        )

        Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="aporte",
            value=Decimal("250.00"),
            quantity=Decimal("5.0"),
            fund=investment_fund_2,
        )

        Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="resgate",
            value=Decimal("100.00"),
            quantity=Decimal("2.0"),
            fund=investment_fund_2,
        )

        url = reverse("wallet-summary")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["total_balance"]) == Decimal("1150.00")
        assert len(response.data["funds"]) == 2

        fund1_data = next(
            fund for fund in response.data["funds"] if fund["ticker"] == "TEST1"
        )
        fund2_data = next(
            fund for fund in response.data["funds"] if fund["ticker"] == "TEST2"
        )

        assert fund1_data["name"] == "Fundo de Teste 1"
        assert Decimal(fund1_data["total_quantity"]) == Decimal("10.0")
        assert Decimal(fund1_data["estimated_value"]) == Decimal("1000.00")

        assert fund2_data["name"] == "Fundo de Teste 2"
        assert Decimal(fund2_data["total_quantity"]) == Decimal("3.0")
        assert Decimal(fund2_data["estimated_value"]) == Decimal("150.00")

    def test_empty_wallet(self, api_client):
        url = reverse("wallet-summary")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["total_balance"]) == Decimal("0")
        assert len(response.data["funds"]) == 0
