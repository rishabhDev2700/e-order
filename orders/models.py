from django.db import models

from accounts.models import User
from store.models import Item


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    total = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=22, unique=True)
    objects = models.Manager()

    def __str__(self) -> str:
        return f'Order by :{self.user} createdon:{self.created_on.date()} total:{self.total}'

    class Meta:
        ordering = ['-created_on']


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self) -> str:
        return f'Item:{self.item.name} qnty:{self.quantity}'
