from django.db import models
from accounts.models import User
from store.models import Item


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    total = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    objects = models.Manager()


class PaymentOrder(models.Model):
    pay_id = models.CharField(max_length=22)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
