import pytest
from django.urls import reverse

from orders.models import Order, OrderItem


@pytest.mark.django_db
def test_order_list_view(client):
    response = client.get('/orders/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_order_create_view(client):
    data = {
        'table_number': 2,
        'status': 'pending',
        'items-TOTAL_FORMS': '2',
        'items-INITIAL_FORMS': '0',
        'items-MIN_NUM_FORMS': '0',
        'items-MAX_NUM_FORMS': '1000',
        'items-0-name': 'Чай',
        'items-0-price': '5.00',
        'items-0-quantity': '1',
        'items-1-name': 'Пирог',
        'items-1-price': '12',
        'items-1-quantity': '1',
    }
    response = client.post('/orders/create/', data)
    assert response.status_code == 302  # redirect
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.table_number == 2
    assert order.total_price == 17  # 12 + 12



# тест страницы расчета выручки
@pytest.mark.django_db
def test_revenue_view(client):
    Order.objects.create(table_number=1, total_price=100, status='paid')
    response = client.get(reverse('revenue'))
    assert response.status_code == 200
    assert b'100' in response.content


#Тест фильтрации заказов по статусу
@pytest.mark.django_db
def test_order_list_view_status_filter(client):
    Order.objects.create(table_number=1, status='pending')
    Order.objects.create(table_number=2, status='paid')
    response = client.get(reverse('order_list') + '?status=paid')
    assert response.status_code == 200
    assert len(response.context['orders']) == 1
    assert response.context['orders'][0].status == 'paid'
