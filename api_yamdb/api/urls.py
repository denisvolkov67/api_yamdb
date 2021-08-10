from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoriesViewSet)
v1_router.register(r'genres', GenresViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'users', UserViewSet, 'users')
# v1_router.register(r'auth/signup', )
# v1_router.register(r'auth/token', TokenObtainPairView)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/users/', UserViewSet, name='user-list'),
    # path('v1/users/<username>/', UserViewSet, name='user-detail'),
]
