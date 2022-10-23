from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    cover = models.ImageField(upload_to='category_imgs/')
    objects = models.Manager()
    slug = models.SlugField(max_length=40)

    def get_absolute_url(self):
        return reverse('store:show_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='item_imgs/')
    price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False)
    objects = models.Manager()
    slug = models.SlugField(max_length=40)

    def get_absolute_url(self):
        return reverse('store:item_details', args=[self.slug])

    def __str__(self):
        return self.name
