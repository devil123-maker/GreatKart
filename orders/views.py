from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment
import datetime


from django.conf import settings

import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store:store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price) * (cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = tax + total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            context = {
                'order' : order ,
                'cart_items': cart_items,
                'tax' : tax , 
                'total' : total ,
                'grand_total' : grand_total ,
            }
            return render(request,'orders/payment.html',context)
        else:
            return redirect('carts:checkout')
    
def payment(request):
    return render(request,'orders/payment.html')

import stripe 
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    
    # Error handling: Don't allow checkout if cart is empty
    if not cart_items.exists():
        return redirect('cart_detail') # Redirect back to cart page

    line_items = []
    total_price_paise = 0  # We calculate in paise (cents) to avoid float issues

    for item in cart_items:
        # Calculate unit amount in paise (e.g., ₹500.50 -> 50050)
        unit_amount = int(item.product.price * 100)
        total_price_paise += unit_amount * item.quantity

        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.product_name,
                },
                'unit_amount': unit_amount,
            },
            'quantity': item.quantity,
        })

    # Create the Stripe Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/order/success/',
        cancel_url='http://127.0.0.1:8000/order/cancel/',
        # CRITICAL: Pass the user ID so the webhook knows whose cart to clear
        metadata={
            "user_id": current_user.id
        }
    )

    # Create the Payment record in 'pending' status
    # We store the session.id to match it later in the webhook
    Payment.objects.create(
        user=current_user,
        payment_id=session.id,   
        amount_paid=total_price_paise / 100, # Convert back to Rupees for DB
        status='pending'
    )

    return redirect(session.url, code=303)

def success(request):
    return render(request,'orders/success.html')

def cancel(request):
    return render(request,'orders/fail.html')

@csrf_exempt
def stripe_webhook(request):
    try:
        payload = request.body
        event = json.loads(payload)

        print("EVENT:", event.get('type'))

        if event.get('type') == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session.get('id')

            print("SESSION ID:", session_id)

            payment = Payment.objects.filter(payment_id=session_id).first()
            if not payment:
                print("❌ Payment not found for:", session_id)
                return HttpResponse(status=200)  # don't crash

            print("PAYMENT USER:", payment.user)

            payment.status = 'paid'
            payment.payment_method = 'Stripe'
            payment.save()

            deleted_count, _ = CartItem.objects.filter(user=payment.user).delete()
            print(f"🧹 Cart cleared items: {deleted_count}")

        return HttpResponse(status=200)

    except Exception as e:
        print("❌ WEBHOOK ERROR:", repr(e))
        return HttpResponse(status=500)