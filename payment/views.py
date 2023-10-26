from storeapp.models import Product, Cart, Cartitems, Category, SavedItem
import json
from django.contrib.auth.decorators import login_required
from storeapp import views
from UserProfile.models import Address
from storeapp.forms import AddressForm
import stripe
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.contrib import messages


from order.views import payment_confirmation
from storeapp.basket import Basket


from django.shortcuts import render
from django.conf import settings



def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

# Create your views here.
@login_required(login_url='UserProfile:signin')
def BasketView(request):
    form = None
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    customer = request.user.customer
    customer_address = Address.objects.filter(customer=customer)
    total = str(cart.cart_total)
    total = total.replace('.', '')
    total =int(total)
    print('total')
    if customer_address:
        print(customer_address)
    else:
        form = AddressForm()
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.customer = request.user.customer
                address.save()

                messages.info(request, 'Shipping info saved')



    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    context = {'cart': cart, 'form':form,'cartitems':cartitems, 'customer_address': customer_address, 'client_secret': intent.client_secret}
    return render(request, 'payment/home.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
