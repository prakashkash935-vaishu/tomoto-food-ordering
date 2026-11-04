
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Order


def indexpage(request):
    return render(request, "index.html")


def whytomoto(request):
    return render(request, "whytomoto.html")


# CUSTOMER REGISTRATION
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if Customer.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        Customer.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register.html")


# CUSTOMER LOGIN
def customerlogin(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("menu")

        messages.error(request, "Invalid username or password!")

    return render(request, "login.html")


# CUSTOMER LOGOUT
@login_required(login_url="login")
def customerlogout(request):
    logout(request)
    return redirect("index")


# FOOD MENU
def menu(request):
    foods = [
        {
            "name": "Chicken Biryani",
            "price": 180,
            "category": "Biryani",
            "image": "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=600"
        },
        {
            "name": "Veg Biryani",
            "price": 140,
            "category": "Biryani",
            "image": "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=600"
        },
        {
            "name": "Chicken Burger",
            "price": 120,
            "category": "Fast Food",
            "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600"
        },
        {
            "name": "Pizza",
            "price": 220,
            "category": "Fast Food",
            "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600"
        },
        {
            "name": "French Fries",
            "price": 90,
            "category": "Snacks",
            "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600"
        },
        {
            "name": "Ice Cream",
            "price": 80,
            "category": "Desserts",
            "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600"
        }
    ]

    return render(request, "menu.html", {
        "foods": foods
    })


# ADD TO CART
def add_to_cart(request):
    if request.method == "POST":
        name = request.POST.get("name")
        
        try:
            price = int(request.POST.get("price", 0))
        except (ValueError, TypeError):
            messages.error(request, "Invalid food price!")
            return redirect("menu")

        if not name or price <= 0:
            messages.error(request, "Invalid food item!")
            return redirect("menu")

        cart_items = request.session.get("cart", {})

        if name in cart_items:
            cart_items[name]["quantity"] += 1
        else:
            cart_items[name] = {
                "name": name,
                "price": price,
                "quantity": 1
            }

        request.session["cart"] = cart_items
        request.session.modified = True

        messages.success(request, "Item added to cart!")

    return redirect("menu")


# VIEW CART
def cart(request):
    cart_items = request.session.get("cart", {})

    total = sum(
        int(item["price"]) * int(item["quantity"])
        for item in cart_items.values()
    )

    count = sum(
        int(item["quantity"])
        for item in cart_items.values()
    )

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total,
        "count": count
    })


# UPDATE CART QUANTITY
def update_cart(request, name):
    if request.method == "POST":
        cart_items = request.session.get("cart", {})

        if name in cart_items:
            action = request.POST.get("action")

            if action == "increase":
                cart_items[name]["quantity"] += 1

            elif action == "decrease":
                cart_items[name]["quantity"] -= 1

                if cart_items[name]["quantity"] <= 0:
                    del cart_items[name]

        request.session["cart"] = cart_items
        request.session.modified = True

    return redirect("cart")


# REMOVE FROM CART
def remove_from_cart(request, name):
    if request.method == "POST":
        cart_items = request.session.get("cart", {})

        if name in cart_items:
            del cart_items[name]

        request.session["cart"] = cart_items
        request.session.modified = True

    return redirect("cart")


# CHECKOUT
@login_required(login_url="login")
def checkout(request):
    cart_items = request.session.get("cart", {})

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("menu")

    total = sum(
        int(item["price"]) * int(item["quantity"])
        for item in cart_items.values()
    )

    payment_options = [
        "Cash on Delivery",
        "Google Pay",
        "PhonePe",
        "Paytm",
        "Debit / Credit Card",
    ]

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        if payment_method not in payment_options:
            messages.error(request, "Please select a valid payment method!")
            return redirect("checkout")

        order = Order.objects.create(
            customer=request.user,
            customer_name=customer_name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            items=cart_items,
            total=total,
            payment_method=payment_method
        )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })


# ORDER SUCCESS
@login_required(login_url="login")
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(request, "order_success.html", {
        "order": order
    })


# MY ORDERS
@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    return render(request, "my_orders.html", {
        "orders": orders
    })


# CUSTOMER PROFILE
@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        if Customer.objects.filter(username=username).exclude(
            id=request.user.id
        ).exists():
            messages.error(request, "Username already exists!")

        elif Customer.objects.filter(email=email).exclude(
            id=request.user.id
        ).exists():
            messages.error(request, "Email already exists!")

        else:
            request.user.username = username
            request.user.email = email
            request.user.phone = phone
            request.user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

    return render(request, "profile.html")
