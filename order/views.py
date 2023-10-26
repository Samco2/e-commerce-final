from django.http.response import JsonResponse
from django.shortcuts import render
from storeapp.models import Product, Cart, Cartitems, Category, SavedItem
from storeapp import views
from UserProfile.models import Address
from storeapp.forms import AddressForm


from .models import Order, OrderItem
from storeapp.basket import Basket

def add(request):
    basket = Basket(request)
    form = None
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    customer = request.user.customer
    customer_addresses = Address.objects.filter(customer=customer)

    for address in customer_addresses:
        home_address = address.home_address
        bus_stop = address.bus_stop
        city = address.city
        state = address.state
        phone = address.phone
        zip_code = address.post_code

    total = str(cart.cart_total)
    # the 'post' is got from ajex action
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = cart.cart_total

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            #collecting primary keys from posted order
            order = Order.objects.create(user_id=user_id, full_name=customer.first_name,
                                address1= home_address,
                                address2= bus_stop, city= city, state = state,
                                phone = phone, post_code = zip_code,
                                total_paid=baskettotal, order_key=order_key)
            # comparing the obtained info with database info
            order_id = order.pk

            # Use sessions data to save some order info to database
            for item in cartitems:
                OrderItem.objects.create(order_id=order_id, product=item.product, price=item.product.price, quantity=item.quantity)
        response = JsonResponse({'success': 'Return something'})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
