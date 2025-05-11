from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InvestmentFundViewSet,
    TransactionViewSet,
    WalletSummaryView,
    APIRootView,
)

router = DefaultRouter()
router.root_view_name = "api-root"
router.register(r"investment-funds", InvestmentFundViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path("", include(router.urls)),
    path("wallet/summary/", WalletSummaryView.as_view(), name="wallet-summary"),
]
