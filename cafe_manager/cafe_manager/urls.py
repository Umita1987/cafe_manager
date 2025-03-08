"""
URL configuration for cafe_manager project.

Определяет маршруты для:
- Django Admin панели `/admin/`
- Веб-интерфейса управления заказами `/orders/`
- REST API `/api/`

Дополнительная документация:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns: list = [
    path('admin/', admin.site.urls, name="admin"),  # 🔹 Django Admin
    path('orders/', include('orders.urls')),  # 🔹 Основной интерфейс кафе
    path('api/', include('orders.api_urls')),  # 🔹 API для работы с заказами
]
