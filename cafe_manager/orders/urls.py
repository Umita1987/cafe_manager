from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    RevenueView
)

# 🔹 Основные маршруты для управления заказами в кафе
urlpatterns: list[path] = [
    path('', OrderListView.as_view(), name='order_list'),         # 📜 Список заказов
    path('create/', OrderCreateView.as_view(), name='order_create'),  # ➕ Создание заказа
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),  # ✏️ Редактирование заказа
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),  # ❌ Удаление заказа
    path('revenue/', RevenueView.as_view(), name='revenue'),      # 💰 Просмотр общей выручки
]
