import pytest
from orders.forms import OrderForm

@pytest.mark.django_db
def test_order_form_invalid():
    form = OrderForm(data={})
    assert not form.is_valid()
    assert 'table_number' in form.errors

@pytest.mark.django_db
def test_order_form_valid():
    form = OrderForm(data={'table_number': 1, 'status': 'pending'})
    assert form.is_valid()
