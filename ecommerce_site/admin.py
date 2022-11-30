from unicodedata import category
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from ecommerce_site.models import *
from django.template.defaultfilters import truncatechars
from ecommerce_site import models
# from import_export.admin import ImportExportModelAdmin
# Register your models here.

# ------------------CATEGORY MODEL-------------------------

class Category_data(admin.ModelAdmin):
    
    def Image(self, obj):
        return format_html('<img src="{}" width="40%" height="20%" />'.format(obj.category_image.url))
    Image.short_description='Image'
    Image.allow_tag=True
    
    def make_active(modeladmin, request, queryset):
        queryset.update(category_status='active')
    make_active.short_description = "Active Selected Category"
    
    def make_inactive(modeladmin, request, queryset):
        # print(queryset)
        queryset.update(category_status='inactive')
    make_inactive.short_description = "Inactive Selected Products"
    
    list_display=('id','Image','category','category_status','created_on','updated_on')
    list_display_links=("category",)
    list_filter = ['category','updated_on']
    search_fields=['category','category_status']
    ordering=('created_on',)
    list_per_page = 10
    actions = [make_active,make_inactive]
admin.site.register(Category,Category_data)

# ------------------PRODUCT MODEL-------------------------

class Product_data(admin.ModelAdmin):
        
    def short_description(self,obj):
        return truncatechars(obj.product_description, 35)
    
    def Image(self, obj):
        return format_html('<img src="{}" width="40%" height="20%" />'.format(obj.product_image.url))
    Image.short_description='Image'
    Image.allow_tag=True
    
    def make_active(modeladmin, request, queryset):
        queryset.update(product_status='active')
    make_active.short_description = "Active Selected Products"
    
    def make_inactive(modeladmin, request, queryset):
        queryset.update(product_status='inactive')
    make_inactive.short_description = "Inactive Selected Products"
    
    list_display_links=("Image","product")
    list_display=('id','Image','product','category_id','short_description','product_price','product_status','product_quantity','created_on','updated_on')
    list_filter = ['category_id','created_on','updated_on']
    list_per_page = 10
    search_fields=('product','category_id')
    ordering=('created_on','updated_on')
    search_fields = ['product', 'product_price']
    readonly_fields=('Image',)
    actions = [make_active,make_inactive]
admin.site.register(Product,Product_data)

# ------------------USER MODEL-------------------------

class UserAdmin(admin.ModelAdmin):
    list_display=('id','first_name','last_name','email')
    list_display_links=('id',"first_name",)
admin.site.register(User,UserAdmin)

# ------------------CART MODEL-------------------------

class CartData(admin.ModelAdmin):
    list_display=('id','user','product','quantity','created_on','updated_on','is_deleted')
    search_fields=['user','product']
    list_display_links=('id',"user",)
    ordering=('created_on','updated_on')
admin.site.register(Cart,CartData)

# ------------------WISHLIST MODEL-------------------------

class WishlistData(admin.ModelAdmin):
    list_display=('id','user','product','created_on')
    list_display_links=("user",)
    ordering=('created_on','updated_on')
admin.site.register(Wishlist,WishlistData)

# ------------------ORDERS MODEL-------------------------

class Order_Items(admin.ModelAdmin):
    list_display=('id','user','address','city','zipcode','ordered_date','delivered_by','order_status')
    ordering=('ordered_date','delivered_by','order_status')
    list_display_links=('id',"user",)
admin.site.register(OrderItems,Order_Items)

admin.site.register(SubscribedUsers)


class Rating_data(admin.ModelAdmin):
    list_display=('id','user','product','ratings')
    list_display_links=("user")
admin.site.register(Rating)
    