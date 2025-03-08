from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Конфигурация приложения 'orders'.

    - 🔹 `default_auto_field`: Определяет тип поля для автоинкрементных ID.
    - 🔹 `name`: Название приложения, используемое в настройках Django.
    """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'orders'
