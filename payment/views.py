import razorpay
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from core import settings
from orders.bag import Bag
from orders.models import Order
from payment.models import PaymentOrder

client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET_KEY))


def create_payment_order(request):
    amount = Bag(request).get_subtotal()
    razorpay_order = client.order.create(dict(
        amount=amount,
        currency='INR',
        payment_capture='0')
    )
    order = Order.objects.create(
        user=request.user,
        total=amount,
        razorpay_order_id=razorpay_order['id']
    )
    payment_order = PaymentOrder(
        order=order,
        user=request.user,
        payment_order_id=razorpay_order['id'],
        amount=amount,
    )
    payment_order.save()
    callback_url = 'paymenthandler/'
    context = {'razorpay_order_id': razorpay_order['id'], 'razorpay_merchant_key': settings.RAZORPAY_ID,
               'razorpay_amount': amount*100, 'currency': 'INR', 'callback_url': callback_url}
    return render(request, 'payment/checkout.html', context=context)


# noinspection PyBroadException
@csrf_exempt
def payment_handler(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            data = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            result = client.utility.verify_payment_signature(data)
            if result is not None:
                order = Order.objects.filter(razorpay_order_id=order_id, user=request.user)
                try:
                    client.payment.capture(payment_id, order.total*100)
                    payment_order = PaymentOrder.objects.get(order=order)
                    payment_order.verified = True
                    payment_order.payment_id = payment_id
                    payment_order.signature = signature
                    payment_order.save()
                    return render(request, 'payment/payment_success.html')
                except:
                    return render(request, 'payment/payment_fail.html')
            else:
                return render(request, 'payment/payment_fail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
