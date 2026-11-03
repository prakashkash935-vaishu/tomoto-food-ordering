
from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexpage, name="index"),
    path("why-tomoto/", views.whytomoto, name="whytomoto"),
    path("register/", views.register, name="register"),
    path("login/", views.customerlogin, name="login"),
    path("logout/", views.customerlogout, name="logout"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/<str:name>/", views.update_cart, name="update_cart"),
path("remove-from-cart/<str:name>/", views.remove_from_cart, name="remove_from_cart"),
path("checkout/", views.checkout, name="checkout"),

path("checkout/", views.checkout, name="checkout"),
path("order-success/<int:order_id>/", views.order_success, name="order_success"),
path("my-orders/", views.my_orders, name="my_orders"),
path("profile/", views.profile, name="profile"),
]
