# models.py
from django.db import models

# payments data to be injected to the database
class Payment(models.Model):
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    result_desc = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
