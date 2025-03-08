from django.db import models
from decimal import Decimal


class Order(models.Model):
    """
    Модель заказа в кафе.

    Атрибуты:
    - 🔹 `table_number` (int) — номер стола, для которого оформлен заказ.
    - 🔹 `total_price` (Decimal) — общая стоимость заказа, пересчитывается автоматически.
    - 🔹 `status` (str) — статус заказа (`в ожидании`, `готово`, `оплачено`).
    """

    STATUS_CHOICES: list[tuple[str, str]] = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: models.IntegerField = models.IntegerField(verbose_name="Номер стола")
    total_price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Общая стоимость")
    status: models.CharField = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")

    def __str__(self) -> str:
        return f"Заказ {self.id} (Стол {self.table_number})"

    def calculate_total(self) -> None:
        """Пересчитывает сумму заказа на основе стоимости блюд."""
        self.total_price = sum(item.price * item.quantity for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    """
    Модель элемента заказа (блюда).

    Атрибуты:
    - 🔹 `order` (ForeignKey) — ссылка на заказ, к которому относится блюдо.
    - 🔹 `name` (str) — название блюда.
    - 🔹 `price` (Decimal) — цена блюда за единицу.
    - 🔹 `quantity` (int) — количество единиц блюда в заказе.
    """

    order: models.ForeignKey = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    name: models.CharField = models.CharField(max_length=100, verbose_name="Название блюда")
    price: models.DecimalField = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self) -> str:
        return f"{self.name} - {self.quantity} шт."
