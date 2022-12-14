import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from orders.models import Order, OrderItem
from store.models import Item, Category
from store_admin.forms import CategoryForm, ItemForm


def dashboard(request):
    date = datetime.date.today()
    incompleted_orders = Order.objects.filter(is_completed=False)
    orders = []
    for order in incompleted_orders:
        order_items = OrderItem.objects.filter(order=order)
        orders.append([order, order_items])
    context = {'date': date, 'orders': orders}
    return render(request, 'store_admin/dashboard.html', context=context)


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
            redirect('store_admin:all_categories')
        else:
            messages.error(request, 'Some Error Occurred!! Please Try Again.')
    form = CategoryForm()
    date = datetime.date.today()
    context = {'title': 'Add Category', 'form': form, 'date': date}
    return render(request, 'store_admin/form.html', context=context)


def category_update(request, slug):
    category = Category.objects.get(slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully')
            redirect('store_admin:dashboard')
        else:
            messages.error(request, "Some Error Occurred!! Please Try Again")
    form = CategoryForm(instance=category)
    date = datetime.date.today()
    context = {'title': 'Update Category', 'form': form, "date": date}
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
    return redirect('store_admin:all_categories')


def all_categories(request):
    categories = Category.objects.all()
    date = datetime.date.today()
    context = {'title': 'Categories', 'categories': categories, 'date': date}
    return render(request, 'store_admin/all_categories.html', context=context)


def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Added Successfully")
            return redirect('store_admin:all_items')
    form = ItemForm()
    date = datetime.date.today()
    context = {'title': 'Add Item', 'form': form, 'date': date}
    return render(request, 'store_admin/form.html', context=context)


def item_update(request, slug):
    item = Item.objects.get(slug=slug)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Update Successfully")
            return redirect('store_admin:dasboard')
        else:
            messages.error(request, "Some Error Occurred!!")
    form = ItemForm(instance=item)
    date = datetime.date.today()
    context = {'title': 'Update Item', 'form': form, 'date': date}
    return render(request, 'store_admin/form.html', context=context)


# noinspection PyBroadException
def item_delete(request):
    item_id = request.POST['item_id']
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        messages.success(request, "Item deleted Successfully")
    except:
        messages.error(request, 'Some Error Occurred')
    return redirect('store_admin:all_items')


def all_items(request):
    items = Item.objects.all()
    date = datetime.date.today()
    context = {'title': 'All Items', 'items': items, 'date': date}
    return render(request, 'store_admin/all_objects.html', context=context)


def view_orders(request):
    date = datetime.date.today()
    all_orders = Order.objects.all()
    completed_orders = all_orders.filter(is_completed=True)
    incompleted_orders = all_orders.filter(is_completed=True)
    orders = []
    for order in completed_orders:
        order_items = OrderItem.objects.filter(order=order)
        orders.append([order, order_items])
    context = {'date': date}
    return render(request, 'store_admin/orders.html', context=context)
