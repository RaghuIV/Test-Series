from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # API routes
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('app.urls')),
    # API schema generation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Optional Redoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
