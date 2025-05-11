import pytest
from decimal import Decimal
from core.models import InvestmentFund, Transaction
import datetime


@pytest.mark.django_db
class TestInvestmentFund:
    def test_investment_fund_creation(self):
        fund = InvestmentFund.objects.create(
            name="Fundo Exemplo",
            ticker="FNDO11",
            fund_type="FII",
            unit_price=Decimal("100.50"),
        )

        assert fund.id is not None
        assert fund.name == "Fundo Exemplo"
        assert fund.ticker == "FNDO11"
        assert fund.fund_type == "FII"
        assert fund.unit_price == Decimal("100.50")

        assert str(fund) == "Fundo Exemplo (FNDO11)"


@pytest.mark.django_db
class TestTransaction:
    def test_transaction_creation(self):
        fund = InvestmentFund.objects.create(
            name="Fundo Teste",
            ticker="TEST11",
            fund_type="FII",
            unit_price=Decimal("50.25"),
        )

        transaction = Transaction.objects.create(
            date=datetime.date.today(),
            transaction_type="aporte",
            value=Decimal("1000.00"),
            quantity=Decimal("19.9004"),
            fund=fund,
        )

        assert transaction.id is not None
        assert transaction.transaction_type == "aporte"
        assert transaction.value == Decimal("1000.00")
        assert transaction.quantity == Decimal("19.9004")
        assert transaction.fund == fund

        expected_str = f"Aporte - Fundo Teste - {datetime.date.today()}"
        assert str(transaction) == expected_str
