from django.conf import settings
from django.db import models

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"Income: {self.amount} on {self.date} by {self.user}"

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"Expense: {self.amount} on {self.date} by {self.user} (Category: {self.category})"
