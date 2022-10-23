from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from orders.bag import Bag
from store.models import Item


# Create your views here.
def bag_summary(request):
    bag = Bag(request)
    context = {'bag': bag}
    return render(request, 'orders/summary.html', context=context)


def bag_add(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        item = get_object_or_404(Item, id=item_id)
        bag.add(item=item, quantity=quantity)

        bag_quantity = bag.__len__()
        response = JsonResponse({"quantity": bag_quantity})
        return response


def bag_delete(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        bag.delete(item=item_id)

        bag_quantity = bag.__len__()
        bag_total = bag.get_subtotal()
        response = JsonResponse({"quantity": bag_quantity, "subtotal": bag_total})
        return response


def bag_update(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("productid"))
        quantity = int(request.POST.get("productqty"))
        bag.update(item=item_id, quantity=quantity)

        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse({"qty": bag_quantity, "subtotal": bag_subtotal})
        return response
