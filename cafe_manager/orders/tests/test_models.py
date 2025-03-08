import pytest

from orders.models import Order, OrderItem


@pytest.mark.django_db
def test_order_creation():
    order = Order.objects.create(table_number=1, status='pending')
    assert order.total_price == 0

@pytest.mark.django_db
def test_order_total_calculation():
    order = Order.objects.create(table_number=5, status='pending')
    OrderItem.objects.create(order=order, name='Пицца', price=30, quantity=2)
    OrderItem.objects.create(order=order, name='Кола', price=5, quantity=3)
    order.calculate_total()

    assert order.total_price == 75 # 2 блюда: (1*30) + (3*5)
