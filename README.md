# Cafe Manager - Django Web & API

## 📌 Описание

**Cafe Manager** — это веб-приложение на Django для управления заказами в кафе. Приложение поддерживает:

- Создание, редактирование и удаление заказов.
- Ведение списка блюд для каждого заказа.
- Подсчет общей суммы заказа.
- Управление статусом заказа ("в ожидании", "готово", "оплачено").
- Фильтрацию и поиск заказов.
- Вычисление выручки за смену.
- REST API для взаимодействия с заказами.

---

## ⚙️ Технологии

- **Python** 3.8+
- **Django** 5.1
- **Django REST Framework** (DRF)
- **drf-yasg** (Swagger-документация)
- **PostgreSQL (База данных)
- **Bootstrap 5** (UI)

---

## 🚀 Установка и запуск

### 🔹 1. Клонирование репозитория

```bash
git clone https://github.com/Umita1987/cafe_manager.git
cd cafe_manager

### 🔹 2. Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate   # Windows

```
### 🔹 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 🔹 4. Настройка базы данных

В проекте используется **PostgreSQL**. Вместо .example.env  создайте свой .env файл со следующими данными:
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

Применение миграций:

```bash
python manage.py migrate
```

### 🔹 5. Создание суперпользователя (для админки)

```bash
python manage.py createsuperuser
```

### 🔹 6. Запуск сервера

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

---

## 🌐 Функционал

### 1️⃣ Веб-интерфейс

- **Главная страница**: http://127.0.0.1:8000/orders/ (список всех заказов).
- **Создание заказа**: http://127.0.0.1:8000/orders/create/.
- **Редактировани заказа** : http://127.0.0.1:8000/orders/{id}/update/
- **Удаление заказов**: http://127.0.0.1:8000/orders/{id}/delete/
- **Страница выручки за смену**: http://127.0.0.1:8000/orders/revenue/ (сумма оплаченных заказов).

### 2️⃣ REST API

Полноценный **CRUD API** для работы с заказами:

- **http://127.0.0.1:8000/api/orders/** — получить список заказов
- **POST /api/orders/** — создать заказ
- **GET /api/orders/{id}/** — получить заказ
- **PUT /api/orders/{id}/** — полностью обновить заказ
- **PATCH /api/orders/{id}/** — частично обновить заказ
- **DELETE /api/orders/{id}/** — удалить заказ

Документация и тестирование: 🔹 **Swagger UI**: http://127.0.0.1:8000/api/swagger/ 
🔹 **ReDoc**: `http://127.0.0.1:8000/api/redoc/`

Пример запроса **PATCH** для обновления блюда в заказе:

```json
{
  "items": [
    { "id": 15, "price": 35.00 }
  ]
}
```

Пример запроса **PUT** (полное обновление заказа):

```json
{
  "table_number": 12,
  "status": "paid",
  "items": [
    { "id": 36, "name": "Паста", "price": 45, "quantity": 1 },
    { "id": 37, "name": "Кофе", "price": 22, "quantity": 1 }
  ]
}
```

## 🛠 Тестирование

Запуск тестов (Pytest):

```bash
pytest
```
