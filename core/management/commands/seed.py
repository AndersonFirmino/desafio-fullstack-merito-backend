from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date

from core.models import InvestmentFund, Transaction


class Command(BaseCommand):
    help = "Seeds the database with example data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting seed process..."))

        # Check if seed has already been applied
        if InvestmentFund.objects.filter(ticker="XPTO11").exists():
            self.stdout.write(
                self.style.SUCCESS("Seed já aplicado. Nada foi alterado.")
            )
            return

        # Create investment funds
        fund1 = InvestmentFund.objects.create(
            name="Fundo Imobiliário XPTO",
            ticker="XPTO11",
            fund_type="FII",
            unit_price=100.00,
        )

        fund2 = InvestmentFund.objects.create(
            name="Fundo Multimercado Alpha",
            ticker="ALPH4",
            fund_type="Multimercado",
            unit_price=250.00,
        )

        # Create transactions for fund1
        Transaction.objects.create(
            date=date.today(),
            transaction_type="aporte",
            value=10000.00,
            quantity=100.0000,
            fund=fund1,
        )

        Transaction.objects.create(
            date=date.today(),
            transaction_type="resgate",
            value=2000.00,
            quantity=20.0000,
            fund=fund1,
        )

        # Create transactions for fund2
        Transaction.objects.create(
            date=date.today(),
            transaction_type="aporte",
            value=25000.00,
            quantity=100.0000,
            fund=fund2,
        )

        Transaction.objects.create(
            date=date.today(),
            transaction_type="resgate",
            value=5000.00,
            quantity=20.0000,
            fund=fund2,
        )

        # Print summary
        funds_count = InvestmentFund.objects.count()
        transactions_count = Transaction.objects.count()

        self.stdout.write(self.style.SUCCESS("Seed completed with success."))
        self.stdout.write(self.style.SUCCESS(f"{funds_count} fundos criados."))
        self.stdout.write(
            self.style.SUCCESS(f"{transactions_count} transações criadas.")
        )
