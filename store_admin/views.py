import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone

from orders.models import Order, OrderItem
from store.models import Item, Category
from store_admin.forms import CategoryForm, ItemForm


def dashboard(request):
    date = datetime.date.today().strftime("%d-%m-%Y")
    current_date = timezone.now()
    orders = Order.objects.filter(created_on__gt=current_date.date())
    incompleted_orders = orders.filter(is_completed=False)
    total_sales = 0
    total_incomplete_orders = incompleted_orders.count()
    for order in orders:
        total_sales+=order.total
    orders = []
    for order in incompleted_orders:
        order_items = OrderItem.objects.filter(order=order)
        orders.append([order, order_items])
    context = {'date': date, 'orders': orders,'total_incomplete_orders':total_incomplete_orders,'total_sales':total_sales}
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
            category = Category.objects.get(id=category_id)
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
            return redirect('store_admin:dashboard')
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
    incompleted = all_orders.filter(is_completed=False)
    incompleted_orders = []
    for order in incompleted:
        items = OrderItem.objects.filter(order=order)
        incompleted_orders.append([order,items])
    completed = all_orders.filter(is_completed=True)
    completed_orders=[]
    for order in completed:
        items = OrderItem.objects.filter(order=order)
        completed_orders.append([order,items])
    context = {'date': date,'completed_orders':completed_orders,'incomplete_orders':incompleted_orders}
    return render(request, 'store_admin/orders.html', context=context)

def sales_today(request):
    current_date = timezone.now()
    start_date = current_date - datetime.timedelta(days=7)
    all_orders = Order.objects.all()
    orders_last_week = all_orders.filter(created_on__range=[start_date,current_date])
    weekly_sales=0
    for order in orders_last_week:
        weekly_sales+=order.total
    orders = all_orders.filter(created_on__gt=current_date.date())
    total_sales = 0
    total_orders = orders.count()
    for order in orders:
        total_sales+=order.total
    title="Sales Today"
    context = {'title':title,'total_orders':total_orders,'total_sales':total_sales,'weekly_sales':weekly_sales}
    return render(request,'store_admin/sales.html',context=context)

def mark_order_status(request):
    if request.method=='POST':
        order_ids = request.POST.getlist('completed_orders[]')
        order_ids = list(map(lambda x: int(x),order_ids))
        Order.objects.filter(id__in=order_ids).update(is_completed=True)
        messages.success(request,"Marked orders successfully!")
        return redirect('store_admin:view_orders')

def unmark_order_status(request):
    if request.method=='POST':
        order_ids = request.POST.getlist('completed_orders[]')
        order_ids = list(map(lambda x: int(x),order_ids))
        Order.objects.filter(id__in=order_ids).update(is_completed=False)
        messages.success(request,"Un-Marked orders successfully!")
        return redirect('store_admin:view_orders')
