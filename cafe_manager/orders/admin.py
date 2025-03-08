from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для заказов"""
    list_display = ("id", "table_number", "total_price", "status")
    list_filter = ("status",)
    search_fields = ("table_number",)
    ordering = ("-id",)
    inlines = []

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админка для блюд в заказе"""
    list_display = ("id", "order", "name", "price", "quantity")
    search_fields = ("name",)
    ordering = ("-id",)

