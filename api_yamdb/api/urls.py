from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import CategoriesViewSet, GenresViewSet, SignupViewSet, TitleViewSet, TokenViewSet, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoriesViewSet)
v1_router.register(r'genres', GenresViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'users', UserViewSet, 'users')
# v1_router.register(r'users/me', UserMeViewSet, 'users')
v1_router.register(r'auth/signup', SignupViewSet, 'signup')
v1_router.register(r'auth/token', TokenViewSet, 'token')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
