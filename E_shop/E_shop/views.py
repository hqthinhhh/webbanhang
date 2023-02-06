from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, Product, Contact_us, Order, Reviews
from django.contrib.auth import authenticate, login
from app.models import UserCreateForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from django.db.models import Avg
import json
import requests
from django.http import HttpResponseRedirect




def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return quote
 
def Master(request):
    quote = get_quote()
    data = {
        'quote': quote
    }
    return render(request, 'master.html',data)



def Index(request):
    category = Category.objects.all().order_by('category_name')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = UserCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Contact_Page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
    return render(request, 'contact.html')


@login_required(login_url="/accounts/login/")
def CheckOut(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

        for i in cart:
            a = (int(cart[i]['price']))
            b = (int(cart[i]['quantity']))
            total = a * b

            order = Order(
                user=user,
                product=(str(cart[i]['name'])),
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                total=total
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')

    return HttpResponse('this is checkout page')


@login_required(login_url="/accounts/login/")
def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user=user)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)


def Product_page(request):
    category = Category.objects.all().order_by('category_name')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
        # review = Reviews.objects.filter(product_re = product)
    else:
        product = Product.objects.all()
    context = {
        'category': category,
        'product': product,
        # 'review': review,
    }
    return render(request, 'product.html', context)


def Product_Detail(request, id):
    category = Category.objects.all().order_by('category_name')
    product = Product.objects.filter(id=id).first()
    categoryID = request.GET.get('category')
    review = Reviews.objects.filter(product_re = product)
    prod = Product.objects.all()
    if request.method=="POST":
        reviews = Reviews(
            name = request.POST.get('name'),
            date = request.POST.get('date'),
            comments = request.POST.get('comments'),
            rate = request.POST.get("rate"),
            product_re = product
        )
        reviews.save()
    avg = Reviews.objects.filter(product_re = product).aggregate(Avg('rate'))
    avg1 = avg["rate__avg"]
    context = {
        'category': category,
        'product': product,
        'review': review,
        'avg1': avg1,
        'prod': prod
    }
    return render(request, 'product_detail.html', context)

# def Review_Pro(request,id):
#     if request.method=="POST":
#         review = Reviews(
#             comments = request.POST.get('comments'),
#             rate = request.POST.get('rate'),
#         )
#         review.save()
#     product = Product.objects.all()
#     review = Reviews.objects.all()
#     context = {
#         'product': product,
#         'review': review,
#     }
#     return render(request, 'product_detail.html', context)


def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product
    }
    return render(request, 'search.html', context)
