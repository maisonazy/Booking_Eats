import json
from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import ReservationForm
from .models import MenuItem, Order, OrderItem

# Create your views here.
def home(request):
    return render(request,'home.html')



def menu(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    query = request.GET.get("q", "").strip()
    if query:
        menu_items = menu_items.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
    categories = MenuItem.CATEGORIES
    return render(request, "menu.html", {"menu_items": menu_items, "categories": categories, "query": query})

def about(request):
    return render(request,'about.html')

def book(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return render(request, "reservation_success.html", {"reservation": reservation})
    else:
        form = ReservationForm()
    return render(request, "book.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("checkout")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("checkout")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def checkout(request):
    errors = []
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not name:
            errors.append("Enter your name.")
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            errors.append("Enter a valid email address.")
        if len(phone) < 7:
            errors.append("Enter a valid phone number.")

        try:
            submitted_items = json.loads(request.POST.get("cart_data", "[]"))
            if not isinstance(submitted_items, list) or not submitted_items:
                raise ValueError
            order_items = []
            for submitted in submitted_items:
                product = MenuItem.objects.filter(slug=submitted.get("id"), is_available=True).first()
                quantity = submitted.get("quantity")
                if not product or not isinstance(quantity, int) or isinstance(quantity, bool) or not 1 <= quantity <= 99:
                    raise ValueError
                order_items.append((product.name, quantity, product.price))
        except (ValueError, TypeError, json.JSONDecodeError, AttributeError):
            order_items = []
            errors.append("Your cart is empty or contains an invalid item. Return to the menu and try again.")

        if not errors:
            total = sum((price * quantity for _, quantity, price in order_items), Decimal("0.00"))
            with transaction.atomic():
                order = Order.objects.create(customer_name=name, email=email, phone=phone, total=total)
                OrderItem.objects.bulk_create([
                    OrderItem(order=order, product_name=product_name, quantity=quantity, unit_price=price)
                    for product_name, quantity, price in order_items
                ])
            return render(request, "order_success.html", {"order": order})

    return render(request, "checkout.html", {"errors": errors})
