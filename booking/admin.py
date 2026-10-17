from django.contrib import admin
from .models import MenuItem, Order, OrderItem, Reservation


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "phone", "total", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer_name", "email", "phone")
    inlines = (OrderItemInline,)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "reservation_date", "reservation_time", "party_size", "phone", "status")
    list_filter = ("status", "reservation_date", "party_size")
    search_fields = ("customer_name", "email", "phone", "special_requests")
    date_hierarchy = "reservation_date"
    list_editable = ("status",)
    readonly_fields = ("created_at",)
