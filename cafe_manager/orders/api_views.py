from typing import Any
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API для управления заказами:
    - ✅ Создание заказа (`POST /api/orders/`)
    - 🔍 Получение списка заказов (`GET /api/orders/`)
    - 📝 Полное обновление (`PUT /api/orders/{id}/`)
    - 🔄 Частичное обновление (`PATCH /api/orders/{id}/`)
    - ❌ Удаление заказа (`DELETE /api/orders/{id}/`)
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="🔄 Частичное обновление заказа. В `items` **обязательно** передавать `id` блюда.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "items": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                            "price": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=35.00),
                        },
                        required=["id"],
                    ),
                )
            },
            required=["items"],
            example={
                "items": [
                    {
                        "id": 15,
                        "price": 35.00
                    }
                ]
            }
        ),
        responses={200: OrderSerializer()},
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        🔄 Частично обновляет заказ:
        - ✅ Можно изменить **только переданные поля**
        - 🍽 **Для блюд (`items`) необходимо передавать `id`**
        - 📌 `PATCH /api/orders/{id}/`
        """
        return super().partial_update(request, *args, **kwargs)
