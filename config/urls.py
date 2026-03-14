from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/products/", include("apps.products.urls")),
    path("api/orders/", include("apps.orders.urls")),
]
