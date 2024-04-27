from django.db import models
from products.models import Product


class Order(models.Model):
    order_number = models.AutoField(primary_key=True, verbose_name='Номер заказа')
    customer_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('GOT', 'Получен'),
        ('SENT', 'Отправлен'),
        ('PROCESSED', 'Обработан'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменен'),

    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SENT')

    # Ссылка на продукт
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name='Продукт')

