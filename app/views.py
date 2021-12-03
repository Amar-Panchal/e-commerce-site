from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        headphone = Product.objects.filter(category='HE')
        Book = Product.objects.filter(category='Bk')
        shoes = Product.objects.filter(category='S')
        sandals = Product.objects.filter(category='Sn')
        watch = Product.objects.filter(category='W')
        Powerbank = Product.objects.filter(category='PW')
        Trimmer = Product.objects.filter(category='T')
        return render(request,'app/home.html',{'topwears':topwears,
        'bottomwears': bottomwears,'mobiles':mobiles,'headphone':headphone,
        'Book':Book,'shoes':shoes,'sandals':sandals,'watch':watch,
        'Trimmer':Trimmer,'Powerbank':Powerbank})


class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) &
            Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product': product,'item_already_in_cart':item_already_in_cart})



@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount +shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'total_amount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)






def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            
            'amount': amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)






def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')


@login_required
def address(request):
    add = Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})



@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})




def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'redmi' or data =='samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles': mobiles})

def topwear(request,data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=400)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=400)
    return render(request, 'app/topwear.html',{'topwears': topwears})

def book(request,data=None):
    if data == None:
        books = Product.objects.filter(category='Bk')
    elif data == 'coding':
        books = Product.objects.filter(category='Bk').filter(brand='coding')
    elif data == 'history':
        books = Product.objects.filter(category='Bk').filter(brand='history')
    return render(request, 'app/book.html',{'books': books})

def trimmer(request,data=None):
    if data == None:
        trimmer = Product.objects.filter(category='T')
    elif data == 'below':
        trimmer = Product.objects.filter(category='T').filter(discounted_price__lt=600)
    elif data == 'above':
        trimmer = Product.objects.filter(category='T').filter(discounted_price__gt=600)
    return render(request, 'app/trimmer.html',{'trimmer': trimmer})

def powerbank(request,data=None):
    if data == None:
        powerbank = Product.objects.filter(category='PW')
    elif data == 'MI' or data =='syska' or data == 'Realme':
        powerbank = Product.objects.filter(category='PW').filter(brand=data)
    elif data == 'below':
        powerbank = Product.objects.filter(category='PW').filter(discounted_price__lt=600)
    elif data == 'above':
        powerbank = Product.objects.filter(category='PW').filter(discounted_price__gt=600)
    return render(request, 'app/powerbank.html',{'powerbank': powerbank})

def bottomwear(request,data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=600)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=600)
    return render(request, 'app/bottomwears.html',{'bottomwear': bottomwear})

def headphone(request,data=None):
    if data == None:
        headphone = Product.objects.filter(category='HE')
    elif data == 'below':
        headphone = Product.objects.filter(category='HE').filter(discounted_price__lt=600)
    elif data == 'above':
        headphone = Product.objects.filter(category='HE').filter(discounted_price__gt=600)
    return render(request, 'app/headphones.html',{'headphone': headphone})
def shoes(request,data=None):
    if data == None:
        shoes = Product.objects.filter(category='S')
    elif data == 'below':
        shoes = Product.objects.filter(category='S').filter(discounted_price__lt=800)
    elif data == 'above':
        shoes = Product.objects.filter(category='S').filter(discounted_price__gt=800)
    return render(request, 'app/shoes.html',{'shoes': shoes})

def sandals(request,data=None):
    if data == None:
        sandals = Product.objects.filter(category='Sn')
    elif data == 'below':
        sandals = Product.objects.filter(category='Sn').filter(discounted_price__lt=800)
    elif data == 'above':
        sandals = Product.objects.filter(category='Sn').filter(discounted_price__gt=800)
    return render(request, 'app/sandals.html',{'sandals': sandals})

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})






@login_required
def checkout(request):
    user= request.user
    add= Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})




@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        x = OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity)
        x.save()
        c.delete()
    return redirect("orders")










@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user= usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form})

            

        