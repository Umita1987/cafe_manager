from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа.

    Поля формы:
    - 🔹 `table_number` (int) — номер стола.
    - 🔹 `status` (str) — статус заказа (`в ожидании`, `готово`, `оплачено`).
    """

    class Meta:
        model: type[Order] = Order
        fields: list[str] = ['table_number', 'status']


# ✅ Формсет для блюд, входящих в заказ
OrderItemFormSet: type = inlineformset_factory(
    Order, OrderItem,
    fields=['name', 'price', 'quantity'],
    extra=1,  # Отображаем 1 пустое поле для добавления нового блюда
    can_delete=True  # Галочка Delete для удаления отдельного блюда в заказе
)
