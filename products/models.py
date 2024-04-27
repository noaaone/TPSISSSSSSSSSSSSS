from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='Название препарата')
    manufacturer = models.CharField(max_length=255, verbose_name='Производитель')
    product_code = models.CharField(max_length=100, verbose_name='Код товара', unique=True)
    supplier_contact = models.CharField(max_length=255, verbose_name='Данные поставщика')
    supplier_country = models.CharField(max_length=100, verbose_name='Страна-поставщик')
    count = models.IntegerField(verbose_name='Количество товаров')  # Заменяем поле status на count

    def __str__(self):
        return f'{self.product_name} ({self.product_code})'



