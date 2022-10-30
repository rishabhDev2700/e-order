from django.shortcuts import render, get_object_or_404

from store.models import Item, Category


# Create your views here.

def home(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_available=True)[:5]
    context = {'categories': categories, 'items': items}
    return render(request, 'store/home.html', context=context)


def show_by_category(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(category=category)
    context = {'title': category.name, 'items': items}
    return render(request, 'store/show_items.html', context=context)


def show_all_categories(request):
    categories = Category.objects.all()
    context = {'title': 'Categories', 'categories': categories}
    return render(request, 'store/categories.html', context=context)


def show_all_items(request):
    items = Item.objects.filter(is_available=True)
    context = {'title': 'All Items', 'items': items}
    return render(request, 'store/show_items.html', context=context)


def item_details(request, slug=None):
    item = get_object_or_404(Item, slug=slug, is_available=True)
    context = {'item': item}
    return render(request, 'store/item_details.html', context=context)
