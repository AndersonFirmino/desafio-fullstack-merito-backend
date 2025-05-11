from django.db import models

# Models will be added here


class InvestmentFund(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    fund_type = models.CharField(max_length=50, db_index=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("aporte", "Aporte"),
        ("resgate", "Resgate"),
    ]

    date = models.DateField(db_index=True)
    transaction_type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPES, db_index=True
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    fund = models.ForeignKey(
        InvestmentFund, on_delete=models.CASCADE, related_name="transactions"
    )

    class Meta:
        indexes = [
            models.Index(fields=["fund", "transaction_type"]),
            models.Index(fields=["date", "fund"]),
        ]

    def __str__(self):
        return (
            f"{self.transaction_type.capitalize()} - " f"{self.fund.name} - {self.date}"
        )
