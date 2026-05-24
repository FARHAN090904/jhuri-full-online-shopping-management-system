from django.db import models
from orders.models import Order


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('mobile_banking', 'Mobile Banking'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('completed', 'Completed'),
        ('failed', 'Failed'), ('refunded', 'Refunded'),
    ]

    payment_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.RESTRICT, db_column='order_id')
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=200, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment {self.payment_id} for Order #{self.order_id}"
