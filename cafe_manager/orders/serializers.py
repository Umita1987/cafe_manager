from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для блюд в заказе.

    Поля:
    - 🔹 `id` (int) — уникальный идентификатор блюда (необязателен при создании).
    - 🔹 `name` (str) — название блюда (необязательно для `PATCH`).
    - 🔹 `price` (Decimal) — цена блюда за единицу (может быть `None` в `PATCH`).
    - 🔹 `quantity` (int) — количество единиц блюда (по умолчанию 1).
    """

    price: serializers.DecimalField = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, required=False)
    name: serializers.CharField = serializers.CharField(required=False)  # ✅ `name` не обязателен для PATCH
    quantity: serializers.IntegerField = serializers.IntegerField(required=False)
    id: serializers.IntegerField = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказов.

    Поля:
    - 🔹 `id` (int) — уникальный идентификатор заказа.
    - 🔹 `table_number` (int) — номер стола.
    - 🔹 `status` (str) — статус заказа (`pending`, `ready`, `paid`).
    - 🔹 `total_price` (Decimal) — общая стоимость заказа (пересчитывается автоматически).
    - 🔹 `items` (list) — список блюд в заказе.
    """

    items: serializers.ListField = OrderItemSerializer(many=True)  # ✅ Вложенный сериализатор

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'total_price', 'items']

    def create(self, validated_data: dict) -> Order:
        """
        🔹 Создает заказ и добавляет к нему блюда.
        """
        items_data: list[dict] = validated_data.pop('items', [])
        order: Order = Order.objects.create(**validated_data)

        # ✅ Создаем блюда, связанные с этим заказом
        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        order.calculate_total()  # ✅ Пересчитываем сумму
        return order

    def update(self, instance, validated_data):
        """Обновление заказа через PUT (полная замена) и PATCH (частичное обновление)"""
        items_data = validated_data.pop('items', None)  # ✅ Извлекаем блюда, если переданы
        print(f"🔍 Получен заказ {instance.id} с блюдами:")
        is_full_update = self.partial is False  # `False` → значит это `PUT`


        # ✅ Если PUT, очищаем список блюд
        if is_full_update and items_data is not None:
            instance.items.all().delete()

        # ✅ Обновляем основные поля заказа (номер стола, статус)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            existing_items = {item.id: item for item in instance.items.all()}  # 🔍 Собираем существующие блюда

            for item_data in items_data:
                item_id = item_data.get("id")

                if item_id:
                    # 🔥 Если блюдо с таким `id` нет в этом заказе → ошибка!
                    if item_id not in existing_items:
                        raise serializers.ValidationError({
                            "items": f"Блюдо с id {item_id} не найдено в этом заказе."
                        })

                    # ✅ Если блюдо существует → обновляем только переданные поля
                    item = existing_items[item_id]
                    for key, val in item_data.items():
                        if key != "id":  # Не обновляем `id`
                            setattr(item, key, val)
                    item.save()

                elif not item_id:
                    # ➕ Если `id` нет, это **НОВОЕ** блюдо → `name` и `price` обязательны
                    if "name" not in item_data or not item_data["name"]:
                        raise serializers.ValidationError({"name": "Name is required for new items."})
                    if "price" not in item_data:
                        raise serializers.ValidationError({"price": "Price is required for new items."})
                    OrderItem.objects.create(order=instance, **item_data)

        instance.calculate_total()  # ✅ Пересчитываем сумму заказа после обновления
        return instance