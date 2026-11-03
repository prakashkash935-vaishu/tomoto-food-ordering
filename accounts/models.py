
from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username


# Order Model
class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    items = models.JSONField(default=dict)
    total = models.PositiveIntegerField()

    payment_method = models.CharField(
        max_length=30,
        default="Cash on Delivery"
    )

    status = models.CharField(
        max_length=30,
        default="Order Placed"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
