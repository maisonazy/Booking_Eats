from django.db import models
from django.utils.text import slugify


class MenuItem(models.Model):
    CATEGORIES = [
        ("burger", "Burger"),
        ("fries", "Fries"),
        ("pasta", "Pasta"),
        ("pizza", "Pizza"),
    ]

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_path = models.CharField(max_length=255, help_text="Path under static/, for example images/bg1.jpeg")
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ("id",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=160)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveSmallIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("reservation_date", "reservation_time")

    def __str__(self):
        return f"{self.customer_name} — {self.reservation_date} {self.reservation_time}"

