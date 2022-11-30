
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
# Create your models here.

active = "active"
inactive = "inactive"
pending = "pending"
delivered = "delivered"
# Create your models here.
STATUS = (
    (active, 'active'), (inactive, 'inactive')
)
ORDER_STATUS = (
    (pending, "pending"), (delivered, "delivered")
)


class Category(models.Model):
    category_image = models.ImageField(upload_to="category")
    category = models.CharField(max_length=20, unique=True)
    category_status = models.CharField(choices=STATUS, max_length=1000)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category
# ----------PRODUCT MODEL--------------------


class Product(models.Model):
    product_image = models.ImageField(upload_to="")
    product = models.CharField(max_length=100, default="Enter Product Name")
    category_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    product_description = models.TextField(
        max_length=1000, default="Enter Product Description")
    product_price = models.IntegerField(default="Enter Product Price")
    product_quantity = models.PositiveIntegerField(max_length=100)
    product_status = models.CharField(choices=STATUS, max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product

# ------------------USER MODEL-----------------------------


class User(AbstractUser):
    username = models.CharField(
        max_length=50, blank=True, null=True, unique=True, default="Username")
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10, default="123-456-789")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
# -------------------------WISHLIST MODEL-----------------------
#  u.user_permissions.add(permission)

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.product.product
# -------------------------ADD TO CART MODEL-----------------------


class Cart(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        print(self.pk)
        return f"{self.quantity} of {self.product.product}"

    def get_total_cost(self):
        total=self.quantity * self.product.product_price
        return str(total)
    
    def get_final_price(self):
        return self.get_total_cost()
    
    def total_all_product_cost(self):
        price=0
        price+=self.quantity*self.product.product_price
        # price=sum(self.get_final_price())
        print(price)
        return price
    def get(self):
        return self.total_all_product_cost()
    
# ------------------------ORDER MODEL-------------------------------------


class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Cart)  # Cart ID
    ordered = models.BooleanField(default=False)
    address = models.TextField(max_length=500, default="address")
    city = models.TextField(max_length=20, default="city")
    zipcode = models.IntegerField(default=0)
    ordered_date = models.DateField(auto_now_add=True)
    delivered_by = models.DateTimeField()
    order_status = models.CharField(choices=ORDER_STATUS, max_length=100)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        # total = 0
        for order_items in self.item.all():
            total += order_items.get(pk=self.pk)

    def get_total_count(self):
        order = OrderItems.objects.get(pk=self.id)
        return order.item.count()
# ------------------------SubscribedUsers MODEL-------------------------------------


class SubscribedUsers(models.Model):
    email = models.CharField(unique=True, max_length=50)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class Rating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ratings=models.IntegerField(default=0)