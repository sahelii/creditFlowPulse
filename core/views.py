from django.shortcuts import render
from rest_framework import viewsets
from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.contrib.auth import authenticate

# Create your views here.

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class PredictCashflowView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()
        days = 30
        balances = []

        # Get all incomes and expenses for the user
        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        # Calculate current balance
        current_balance = Decimal('0.00')
        for inc in incomes:
            if inc.date <= today:
                current_balance += inc.amount
        for exp in expenses:
            if exp.date <= today:
                current_balance -= exp.amount

        # Prepare recurring incomes/expenses
        recurring_incomes = [inc for inc in incomes if inc.is_recurring]
        recurring_expenses = [exp for exp in expenses if exp.is_recurring]

        # Project for the next 30 days
        balance = current_balance
        for i in range(1, days + 1):
            day = today + timedelta(days=i)
            # Add non-recurring incomes/expenses for this day
            for inc in incomes:
                if not inc.is_recurring and inc.date == day:
                    balance += inc.amount
            for exp in expenses:
                if not exp.is_recurring and exp.date == day:
                    balance -= exp.amount
            # Add recurring incomes/expenses if today is the same day of month as the original
            for inc in recurring_incomes:
                if inc.date.day == day.day and day > inc.date:
                    balance += inc.amount
            for exp in recurring_expenses:
                if exp.date.day == day.day and day > exp.date:
                    balance -= exp.amount
            balances.append({"date": str(day), "projected_balance": str(balance)})
        return Response(balances)

class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not username or not email or not password:
            return Response({'error': 'username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class PasswordResetView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                email_template_name='registration/password_reset_email.html',
            )
        # Always return this response for security (do not reveal if email exists)
        return Response({'message': 'If an account with that email exists, a password reset email has been sent.'}, status=status.HTTP_200_OK)

class PasswordUpdateView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        old_password = request.data.get('old_password')
        if not email or not new_password:
            return Response({'error': 'email and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if old_password:
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
