from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoriesViewSet)
v1_router.register(r'genres', GenresViewSet)
v1_router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
