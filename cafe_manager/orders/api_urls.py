from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import OrderViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.renderers import JSONRenderer
from drf_yasg.renderers import SwaggerJSONRenderer, SwaggerYAMLRenderer
from rest_framework.views import APIView

# Конфигурация Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Cafe Manager API",
        default_version='v1',
        description="API для управления заказами в кафе",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@cafe.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Классы для отображения схемы API в разных форматах
class SchemaJsonView(APIView):
    renderer_classes = [SwaggerJSONRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        return schema_view.without_ui(cache_timeout=0)(request, *args, **kwargs)

class SchemaYamlView(APIView):
    renderer_classes = [SwaggerYAMLRenderer]

    def get(self, request, *args, **kwargs):
        return schema_view.without_ui(cache_timeout=0)(request, *args, **kwargs)

# Роутер для API
router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),


    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # JSON/YAML схема API
    path('swagger.json', SchemaJsonView.as_view(), name='schema-json'),
    path('swagger.yaml', SchemaYamlView.as_view(), name='schema-yaml'),
]
