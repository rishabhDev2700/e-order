from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from store.models import Item, Category
from store_admin.forms import CategoryForm, ItemForm


def dashboard(request):
    context = {}
    return render(request, 'store_admin/dashboard.html', context=context)


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
            redirect('dashboard')
        else:
            messages.error(request, 'Some Error Occurred!! Please Try Again.')
    form = CategoryForm()
    context = {'title': 'Add Category', 'form': form}
    return render(request, 'store_admin/form.html', context=context)


def category_update(request, slug):
    category = Category.objects.get(slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully')
            redirect('dashboard')
        else:
            messages.error(request, "Some Error Occurred!! Please Try Again")
    form = CategoryForm(instance=category)
    context = {'title': 'Update Category', 'form': form}
    return render(request, 'store_admin/form.html', context=context)


def category_delete(request):
    if request.method == 'POST':
        try:
            category_id = request.POST['category_id']
            category = Item.objects.get(id=category_id)
            category.delete()
            messages.success(request, "Category Delete Successfully")
        except Http404:
            messages.error(request, "Unable to delete category")
    else:
        messages.error(request, "Invalid request")
    return redirect('dashboard')


def all_categories(request):
    categories = Category.objects.all()
    context = {'title': 'Categories', 'categories': categories}
    return render(request, 'store_admin/all_objects.html', context=context)


def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Added Successfully")
            return redirect('items')
    form = ItemForm()
    context = {'title': 'Add Item', 'form': form}
    return render(request, 'store_admin/form.html', context=context)


def item_update(request, slug):
    item = Item.objects.get(slug=slug)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Update Successfully")
            return redirect('dasboard')
        else:
            messages.error(request, "Some Error Occurred!!")
    form = ItemForm(instance=item)
    context = {'title': 'Update Item', 'form': form}
    return render(request, 'store_admin/form.html', context=context)


# noinspection PyBroadException
def item_delete(request, pk):
    item_id = request.POST['item_id']
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        messages.success(request, "Item deleted Successfully")
    except:
        messages.error(request, 'Some Error Occurred')
    return redirect('dashboard')


def all_items(request):
    items = Item.objects.all()
    context = {'title': 'All Items', 'items': items}
    return render(request, 'store_admin/all_objects.html', context=context)


def view_orders(request):
    context = {}
    return render(request, 'store_admin/orders.html', context=context)
