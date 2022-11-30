from __future__ import print_function
from datetime import date
import datetime
import io
from django.core.mail import EmailMultiAlternatives
from io import BytesIO
import uuid
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from ecommerce_site.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
import os
import csv


def index(request):
    return render(request, 'index.html')


def UserLogin(request):
    return render(request, 'User_Login.html')


def UserSignUp(request):
    return render(request, 'User_SignUp.html')


def Product_Category(request):
    return render(request, "product_by_category.html")


def Order(request):
    cart = Cart.objects.filter(user=request.user.id)
    total = Cart.objects.filter(user=request.user.id, is_deleted=False).count()
    delivery_date = date.today()+datetime.timedelta(days=2)
    return render(request, "checkout.html", {'products': cart, 'total': total, 'delivery_date': delivery_date})


def reset_done(request):
    return render(request, 'password_reset_done.html')


def password_confirmed(request):
    return render(request, 'password_confirmed.html')


@login_required
def Order_History(request):
    order_data = OrderItems.objects.filter(user=request.user.id)
    cart = Cart.objects.filter(user=request.user.id)
    return render(request, 'order_history.html', {'order': cart, 'order_data': order_data})

# ---------------------USER FUNCTIONALITIES -------------------------------------------


def User_Registration(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['Email']).exists():
            messages.success(request, 'Email Already exists')
            return redirect('user_registration')
        user = User.objects.create_user(username=request.POST['Email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['Email'],
                                        password=request.POST['Password'], phone_no=request.POST['Phno'], is_staff=False)
        user.save()
        messages.success(request, 'Registered Successfully')
        return redirect('user_login')
    else:
        messages.success(request, 'Something Went Wrong ')
        return render(request, 'User_SignUp.html')

# ------------USER LOGIN -------------


def User_Login(request):
    if request.method == "POST":
        try:
            user = request.POST['username']
            pwd = request.POST['password']
            if not user or not pwd:
                messages.success(
                    request, 'Both Username and Password are required.')
                return redirect('user_signup')
            user = User.objects.filter(email=user).first()
            if user is not None:
                login(request, user)
                # Render to their Cart/Wishlist/Order/Dashboard page
                return render(request, "index.html")
            else:
                messages.success(request, 'User does not exist')
                return render(request, "User_Login.html")
        except Exception as e:
            print(e)
            messages.info(request, "Something Went Wrong")

# ------------USER LOGOUT  -------------


@login_required
def UserLogout(request):
    logout(request)
    return redirect('ecommerce_site')

# --------------------- PRODUCTS FUNCTIONALITIES -------------------------------------------


def View_all_Products(request):
    products = Product.objects.filter(product_status="active")
    return render(request, 'view_all_products.html', {'products': products})


def view_Products(request):
    category = Category.objects.filter(category_status="active")
    # products = Product.objects.filter(product_status="active")
    return render(request, 'Products.html', {'products': category})


def Product_by_Category(request, pk):
    category_id = Category.objects.get(id=pk)
    print(category_id)
    products = Product.objects.filter(
        category_id=category_id, product_status="active")
    # print(products)
    return render(request, 'product_by_category.html', {'products': products})


def Product_details(request, pk):
    products = Product.objects.filter(id=pk, product_status="active")
    print(products)
    return render(request, 'product_details.html', {'products': products})

# ------------------------ CART FUNCTIONALITIES  --------------------------------------------


@login_required
def Add_to_Cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if(Cart.objects.filter(product=product, user_id=request.user.id).exists()):
        add_cart = Cart.objects.filter(
            product=product, user_id=request.user.id).update(
                quantity=F('quantity')+1)

        # add_cart.save()
        messages.success(request, 'Product Updated Successfully')
        return redirect("view_products")
    else:
        add_cart = Cart.objects.create(
            product=product, user_id=request.user.id, quantity=1)
        add_cart.save()
        messages.success(request, 'Product Added Successfully')
        return redirect("view_products")

# ----DISPLAY CART ITEMS----------


@login_required
def cart_show(request):
    cart = Cart.objects.filter(user_id=request.user.id, is_deleted=False)
    return render(request, 'cart_details.html', {'cart': cart})


@login_required
def Remove_Cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if Cart.objects.filter(product_id=product).exists():
        Cart.objects.filter(product_id=product).delete()
        messages.success(request, 'Product Removed from cart')
        return redirect("cart_data")


def remove_fromcart(request, val):
    product = Product.objects.get(id=val)
    if(Cart.objects.filter(product=product, user_id=request.user.id).exists()):
        add_cart = Cart.objects.filter(
            product=product, user_id=request.user.id).update(
                quantity=F('quantity')-1)
    return HttpResponse("removed")


def update_cart(request, val):
    product = Product.objects.get(id=val)
    if(Cart.objects.filter(product=product, user_id=request.user.id).exists()):
        add_cart = Cart.objects.filter(
            product=product, user_id=request.user.id).update(
                quantity=F('quantity')+1)
    return HttpResponse("Added")

# ---------------------------------- WISHLIST FUNCTIONALITIES ----------------------------------------------


@login_required
def Add_Wishlist(request, product_id):
    if Wishlist.objects.filter(product=product_id, user_id=request.user.id).exists():
        messages.success(request, 'Product Already Wishlisted')
        return redirect("wishlist_data")
    else:
        product = Product.objects.get(id=product_id)
        add_wishlist = Wishlist.objects.create(
            product=product, user_id=request.user.id)
        add_wishlist.save()
        return redirect("wishlist_data")


@login_required
def Wishlist_show(request):
    wishlist = Wishlist.objects.filter(user_id=request.user.id)
    return render(request, 'wishlist_details.html', {'wishlist': wishlist})


@login_required
def Remove_Wishlist(request, product_id):
    if(Wishlist.objects.filter(product=product_id, user_id=request.user.id).exists()):
        wishlist = Wishlist.objects.filter(product=product_id)
        wishlist.delete()
        messages.success(request, 'Product Removed')
        return redirect("wishlist_data")
    else:
        messages.success(request, 'Product Does Not Exists')
        return redirect("wishlist_data")


@login_required
def Confirm_Order(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    print(cart)
    if request.method == "POST":

        delivery_date = date.today()+datetime.timedelta(days=2)
        user = User.objects.get(id=request.user.id)
        order = OrderItems.objects.create(
            user=user, address=request.POST['Address'], city=request.POST['City'], zipcode=request.POST['Zip'], delivered_by=delivery_date, order_status=pending)
        order.save()
        cart.update(is_deleted=True)
        messages.success(request, 'Ordered Successfully')
    return redirect('product_invoice')


@login_required
def Order_Product(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_data = Cart.objects.filter(user_id=request.user.id)
    return render(request, 'checkout.html', {'products': cart_data})


# --------------------------------- PASSWORD UPDATIONS ------------------------------------------


def ForgetPassword(request):

    try:
        if request.method == 'POST':
            username = request.POST['username']
            if not User.objects.filter(username=username).first():
                messages.success(
                    request, 'User does not exist with this UserName')
                return redirect('forget_password')
            else:
                token = str(uuid.uuid4())
                user_obj = User.objects.get(username=username)
                uidb64 = user_obj.id
                subject = 'Forgot Password link'
                message = f'Click on the below link to reset your Password http://127.0.0.1:8002/change_password/{uidb64}/{token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_obj.email, ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('password_confirmed')
    except Exception as e:
        print(e)
    return render(request, 'forget_password.html')

#  -----CONFIRMED PASSWORD --------


def ChangePassword(request, uid64, token):
    context = {}
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.filter(id=uid64).first()
    try:
        User = User.objects.filter(user_id=user.id).first()
        context = {'user_id': User.user_id}
        # print(user)
        if user.id is None:
            messages.success(request, 'User Not Found')
            return redirect(f'change_password.html/{uid64}/{token}')

        if new_password != confirm_password:
            messages.success(
                request, 'Password and Confirm Password must be Same')
            return redirect(f'change_password.html/{uid64}/{token}')

        user.set_password(new_password)
        user.save()
        return redirect('password_confirmed')
    except Exception as e:
        print(e)
    return render(request, 'change_password.html', context)

# ------------------GENERATE INVOICE AND SEND IN USER'S MAIL-----------------------------------


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def GenerateInvoice(request):
    order_db = OrderItems.objects.filter(user=request.user.id).first()
    cart_db = Cart.objects.filter(user=request.user.id,)
    cart = cart_db.reverse()[0]
    # print(cart.quantity)
    product_db = Product.objects.get(product=cart.product)
    print(product_db.product_image)
    template = get_template('invoice.html')
    data = {
        'order_id': order_db.id,
        'items': order_db.item,
        'user_email': request.user.email,
        'order_date': str(order_db.ordered_date),
        'delivery_date': str(order_db.delivered_by),
        'product_image': product_db.product_image,
        'product': product_db,
        'quantity': cart.quantity,
        'price': product_db.product_price,
        'amount': cart.get_final_price(),
    }
    # print(data)
    pdf = render_to_pdf('invoice.html', data)
    # return HttpResponse(pdf),content_type="application/pdf")
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = 'Invoice Famms Online Shopping.pdf'

    mail_subject = 'Recent Order Details'
    context_dict = {
        'user': order_db.user,
        'order': order_db
    }
    template = get_template('invoice.html')
    messages = template.render(context_dict)
    to_email = request.user.email
    email = EmailMultiAlternatives(
        mail_subject,
        "Your Invoice Order",       # necessary to pass some message here
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    email.attach(filename, pdf, 'application/pdf')
    email.send(fail_silently=False)
    return render(request, 'checkout.html')

# # ---------------------------NEWSLETTER SUBSCRIPTION------------------------


def validate_email(request):
    email = request.POST.get("email", None)
    if SubscribedUsers.objects.filter(email=email).exists():
        messages.info(request, " Already Subscripted")
        return redirect("ecommerce_site")
    else:
        if request.method == "POST":
            mail_subscription = SubscribedUsers.objects.create(email=email)
            mail_subscription.save()
            subject = 'NewsLetter Subscription'
            message = f'This email was sent to '+email + \
                '. You can unsubscribe to stop receiving all emails. By unsubscribing, you will no longer receive newsletters or offers.http://127.0.0.1:8000/unsubscribe_newsletter/.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "NewsLetter Subscripted")
            return redirect("ecommerce_site")
        else:
            messages.success(request, "Something Went Wrong")
            return redirect("ecommerce_site")


def Unsubscribe(request):
    email = request
    return HttpResponse(email)
