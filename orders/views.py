from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.utils import timezone

from orders.models import Order
from orders.serializers import OrderSerializer


# Create your views here.

def orders(request, page_number):
    # Определение количества элементов на странице
    items_per_page = 2  # Установите желаемое количество элементов на странице

    # Получение всех заказов
    all_orders = Order.objects.all()

    # Создание объекта Paginator
    paginator = Paginator(all_orders, items_per_page)

    # Получение номера страницы

    try:
        # Получение объектов на указанной странице
        orders_on_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если 'page' не является целым числом, возвращаем первую страницу
        orders_on_page = paginator.page(1)
    except EmptyPage:
        # Если 'page' больше, чем общее количество страниц, возвращаем последнюю страницу
        orders_on_page = paginator.page(paginator.num_pages)

    # Сериализация объектов на странице
    serializer = OrderSerializer(orders_on_page, many=True)

    # Возврат JSON-ответа с данными
    return JsonResponse(serializer.data, safe=False)


def top_sales_by_hours(request):
    return None


def top_sales_intervals(request):
    return None


def general_check(request):
    # Получаем сегодняшнюю дату и время
    now = timezone.now()

    # Получаем количество заказов за сегодняшний день
    order_count = Order.objects.filter(order_date__date=now.date()).count()

    # Возвращаем количество заказов в формате JSON
    return JsonResponse({'order_count': order_count})


def all_check(request):
    return None
