from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer', 'product_code', 'supplier_contact', 'supplier_country', 'count')
    search_fields = ['product_name', 'product_code', 'manufacturer', 'supplier_country']
    list_filter = ['manufacturer', 'supplier_country']