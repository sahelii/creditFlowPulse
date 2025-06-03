from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, ExpenseViewSet, PredictCashflowView, RegisterView, PasswordResetView, PasswordUpdateView, CategoryViewSet, SummaryView, LoginView

router = DefaultRouter()
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    path('predict-cashflow/', PredictCashflowView.as_view(), name='predict-cashflow'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-update/', PasswordUpdateView.as_view(), name='password-update'),
    path('summary/', SummaryView.as_view(), name='summary'),
] 