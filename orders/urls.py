from django.urls import path
from . import views

urlpatterns = [
    path("<int:page_number>/", views.orders, name="orders"),
    path("today/general/", views.general_check, name="average_check_general"),
    path("today/all/", views.all_check, name="average_check_all"),
    path("today/by_hours/", views.top_sales_by_hours, name="top_sales_by_hours"),
    path("today/intervals/", views.top_sales_intervals, name="top_sales_intervals"),
]
