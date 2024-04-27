from django.urls import path
from . import views

urlpatterns = [
    path("sales/", views.sales_statistics_view, name="sales"),
    path("last_orders/", views.recent_orders_view, name="recent_orders"),
    path("check/average/", views.average_check_view, name="average_check"),
    path("top_sales/", views.top_selling_products_view, name="top_sales"),
]
