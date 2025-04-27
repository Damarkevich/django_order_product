from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CompanyViewSet,
    ContactViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
)

router_v1 = DefaultRouter()
router_v1.register(r"companies", CompanyViewSet, basename="companies")
router_v1.register(r"contacts", ContactViewSet, basename="contacts")
router_v1.register(r"orders", OrderViewSet, basename="orders")
router_v1.register(r"order-items", OrderItemViewSet, basename="order-items")
router_v1.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/", include("dj_rest_auth.urls")),
]
