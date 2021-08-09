from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoriesViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]