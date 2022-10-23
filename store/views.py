from django.shortcuts import render, get_object_or_404

from store.models import Item, Category


# Create your views here.
def show_by_category(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(category=category)
    context = {'items': items}
    return render(request, 'store/show_items.html', context=context)


def show_all_items(request):
    items = Item.objects.filter(isAvailable=True)


def item_details(request, slug=None):
    item = get_object_or_404(Item, slug=slug, isAvailable=True)
    context = {'item': item}
    return render(request, 'store/item_details.html', context=context)
