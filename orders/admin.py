from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_cost', 'order_date', 'status', 'product')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer_name', 'product__product_name')  # Поиск по полям order_number, customer_name и product_name
