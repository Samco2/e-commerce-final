import re
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from UserProfile.models import Address
from .forms import CreateUserForm
from storeapp.models import Cart
from django.contrib.auth import authenticate, login, logout
from storeapp.forms import AddressForm
from order.views import user_orders

def signup(request):
    form =  CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account Created! You can Login')
            return redirect('UserProfile:signin')
        else:
            messages.info(request, 'Choose another password')

    context = {'form': form}
    return render(request, 'UserProfile/signup.html', context)

def signin(request):
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            cart.owner = request.user.customer
            cart.save()
            return redirect('payment:home')

        else:
            messages.info(request, 'Invalid credentials')


    print(cart.owner)
    context = {'cart':cart}
    return render(request, 'UserProfile/login.html', context)

def signout(request):
    logout(request)
    return redirect('index')

def changeAddress(request):
    customer = request.user.customer
    address = Address.objects.get(customer=customer)
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.customer = customer
            new_address.save()
            return redirect('payment:home')
    context = {'form':form}
    return render(request, 'UserProfile/updateaddress.html', context)

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'user/dashboard.html', {'orders': orders})
