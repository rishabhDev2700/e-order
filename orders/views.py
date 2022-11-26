from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from orders.bag import Bag
from orders.models import Order
from store.models import Item


# Create your views here.
def bag_summary(request):
    bag = Bag(request)
    context = {'bag': bag}
    return render(request, 'orders/bag_summary.html', context=context)


def bag_add(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        item = get_object_or_404(Item, id=item_id)
        bag.add(item=item, quantity=quantity)
        bag_quantity = bag.__len__()
        response = JsonResponse({"quantity": bag_quantity, 'message': f'{item.name} added'})
        return response


def bag_delete(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        item = get_object_or_404(Item, id=item_id)
        bag.delete(item=item)
        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse({"quantity": bag_quantity, "subtotal": bag_subtotal, 'message': f'{item.name} removed'})
        return response


def bag_update(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        item = get_object_or_404(Item, id=item_id)
        bag.update(item=item, quantity=quantity)
        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse({"quantity": bag_quantity, "subtotal": bag_subtotal, 'message': f'{item.name} updated'})
        return response


def bag_clear(request):
    bag = Bag(request)
    bag.clear()
    return JsonResponse({'quantity': 0, 'subtotal': 0, 'message': 'Bag Cleared'})


def user_orders(request):
    all_orders = Order.objects.filter(user=request.user)
    completed = all_orders.filter(is_completed=True)
    incomplete = all_orders.filter(is_completed=False)
    context = {"completed": completed, "incomplete": incomplete}
    return render(request, 'orders/user_orders.html', context=context)
