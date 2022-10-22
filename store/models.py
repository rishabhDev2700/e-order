from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    cover = models.ImageField(upload_to='category_imgs/')


class Item(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='item_imgs/')
    price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False)
