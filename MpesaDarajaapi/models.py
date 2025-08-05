# models.py
from django.db import models

# payments data to be injected to the database
class Payment(models.Model):
    merchant_request_id = models.CharField(max_length=255, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=255, unique=True)
    result_code = models.IntegerField()
    result_desc = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # MpesaReceiptNumber
    user_phone_number = models.CharField(max_length=20, blank=True, null=True)
    transaction_date = models.CharField(max_length=20, blank=True, null=True)  # YYYYMMDDHHMMSS
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id or 'Pending'} - {self.amount}"
from django.db import models

class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_request_id = models.CharField(max_length=100, null=True, blank=True)
    merchant_request_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"
