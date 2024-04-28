from collections import defaultdict

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import OrderSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_sales_by_hours(request):
    # Получаем текущее время и дату
    now = timezone.now()

    # Получаем начало и конец текущего дня
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Получаем все заказы за сегодня
    all_orders_today = Order.objects.filter(order_date__date=now.date())

    # Получаем все заказы за сегодня, которые были доставлены
    delivered_orders_today = all_orders_today.filter(status='DELIVERED')

    # Вычисляем процент доставленных заказов за сегодня
    if all_orders_today.exists():
        percent_delivered = (delivered_orders_today.count() / all_orders_today.count()) * 100
    else:
        percent_delivered = 0

    # Возвращаем текущий час и процент доставленных заказов за сегодня в формате JSON
    return JsonResponse({'current_hour': now.hour, 'percent_delivered': percent_delivered})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_sales_intervals(request):
    # Получаем текущую дату и время
    now = timezone.now()

    # Определяем интервалы времени
    intervals = [
        (6, 12),  # 6:00 - 12:00
        (12, 18), # 12:00 - 18:00
        (18, 24)  # 18:00 - 0:00 (следующий день)
    ]

    # Создаем словарь для хранения количества заказов для каждого интервала
    order_counts = {}

    # Получаем количество заказов для каждого интервала
    for start_hour, end_hour in intervals:
        # Получаем заказы за сегодня в текущем интервале времени
        orders_in_interval = Order.objects.filter(
            order_date__date=now.date(),
            order_date__hour__range=(start_hour, end_hour - 1)  # -1 чтобы не включать конечное время
        ).count()
        order_counts[f"{start_hour}-{end_hour}"] = orders_in_interval

    # Возвращаем количество заказов для каждого интервала в формате JSON
    return JsonResponse(order_counts)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def general_check(request):
    # Получаем сегодняшнюю дату и время
    now = timezone.now()

    # Получаем количество заказов за сегодняшний день
    order_count = Order.objects.filter(order_date__date=now.date()).count()

    # Возвращаем количество заказов в формате JSON
    return JsonResponse({'order_count': order_count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_check(request):
    # Получаем текущую дату и время
    now = timezone.now()

    # Определяем интервал времени на 25 часов (сегодня и следующий день)
    start_time = timezone.datetime.combine(now.date(), timezone.datetime.min.time())
    end_time = start_time + timezone.timedelta(hours=24)

    # Создаем словарь для хранения суммы заказов для каждого часа, инициализируем его нулевыми значениями
    orders_total_per_hour = defaultdict(float)

    # Создаем словарь для каждого часа и инициализируем его нулевыми значениями
    for hour in range(24):
        orders_total_per_hour[hour] = 0.0

    # Получаем сумму заказов для каждого часа
    orders = Order.objects.filter(order_date__range=(start_time, end_time))
    for order in orders:
        hour = order.order_date.hour
        orders_total_per_hour[hour] += float(order.total_cost)

    # Возвращаем словарь с суммой заказов для каждого часа в формате JSON
    return JsonResponse(dict(orders_total_per_hour))
