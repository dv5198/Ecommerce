from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="Ecommerce"),
    path('ecommerce_site', views.index, name="ecommerce_site"),
    #     -----------USER -----------
    path('user_login/', views.UserLogin, name="user_login"),
    path('user_logout/', views.UserLogout, name="user_logout"),
    path('user_signup/', views.UserSignUp, name="user_signup"),
    path('user_registration/', views.User_Registration,
         name="user_registration"),
    path('user_check/', views.User_Login, name="user_check"),
    #     ------------PRODUCTS---------
    path('view_all_products/', views.View_all_Products, name="view_all_products"),
    path('view_products/', views.view_Products, name="view_products"),
    # view_products/product_by_category/category_id
    path('product_by_category/<str:pk>',
         views.Product_by_Category, name="product_by_category"),
    # path('product_by_category/',views.Product_Category,name="product_by_category"),
    path('product_details/<str:pk>', views.Product_details, name="product_details"),
    # -------------CART AND WISHLIST-----------------
    path('add_to_cart/<str:product_id>', views.Add_to_Cart, name="add_to_cart"),
    path('cart_data/', views.cart_show, name="cart_data"),
    path("add_to_wishlist/<int:product_id>",
         views.Add_Wishlist, name="add_to_wishlist"),
    path("wishlist_data/", views.Wishlist_show, name="wishlist_data"),
    path("remove_from_wishlist/<str:product_id>",
         views.Remove_Wishlist, name="remove_from_wishlist"),
    path("remove_cart/<int:product_id>", views.Remove_Cart, name="remove_cart"),
    path("remove_fromCart/<int:val>",views.remove_fromcart, name="remove_fromCart"),
    path("add_toCart/<int:val>",views.Add_to_Cart, name="remove_fromCart"),
    #     -----------------ORDER CONFIRMATION AND CHECKOUT---------------------------
    path("checkout/", views.Order, name="checkout"),
    path("checkout/<int:product_id", views.Order, name="checkout_all"),
    path("checkout_single/<int:product_id>",
         views.Order_Product, name="checkout_single"),
    path('confirm_order', views.Confirm_Order, name="confirm_order"),
    path('order_history/', views.Order_History, name="order_history"),
    path("product_invoice/", views.GenerateInvoice, name="product_invoice"),
    #     --------------------PASSWORD UPDATIONS----------------------
    path('forget_password/', views.ForgetPassword, name="forget_password"),
#     path('forgetpassword/', views.Forgotpassword, name="forgetpassword"),
    path('change_password/<uid64>/<token>/',
         views.ChangePassword, name="change_password"),
    path("reset_done/", views.reset_done, name="reset_done"),
    path("password_confirmed/", views.password_confirmed,
         name="password_confirmed"),
    #     ---------NEWSLETTER SUBSCRIBE----------
    path('email_subscribe/', views.validate_email, name='email_subscribe'),
    path('unsubscribe_newsletter/', views.Unsubscribe,
         name="unsubscribe_newsletter"),

    
]
