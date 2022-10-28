from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from orders.bag import Bag
from orders.models import Order, OrderItem
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
        response = JsonResponse({"quantity": bag_quantity})
        return response


def bag_delete(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        bag.delete(item=item_id)

        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse({"quantity": bag_quantity, "subtotal": bag_subtotal})
        return response


def bag_update(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        bag.update(item=item_id, quantity=quantity)

        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse({"quantity": bag_quantity, "subtotal": bag_subtotal})
        return response


def order_add(request):
    bag = Bag(request)
    if request.POST.get("action") == 'post':
        order_id = request.POST.get('order_id')
        user_id = request.user.id
        bag_total = bag.get_subtotal()

        if Order.objects.filter(id=order_id).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, total=bag_total)
            order_id = order.pk
            for item in bag:
                OrderItem.objects.create(order_id=order_id,
                                         item=item['item'],
                                         price=item['price'],
                                         quantity=item['quantity'], )
            response = JsonResponse({"success": "some message"})
            return response
