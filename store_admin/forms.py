from django.forms import ModelForm

from store.models import Item, Category


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'cover', 'price', 'is_available', 'slug']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'cover', 'slug']
