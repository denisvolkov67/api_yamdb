from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewsViewSet, SignupViewSet, TitleViewSet, TokenViewSet,
                    UserViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r"users", UserViewSet, "users")
v1_router.register(r"auth/signup", SignupViewSet, "signup")
v1_router.register(r"auth/token", TokenViewSet, "token")
v1_router.register(r"categories", CategoriesViewSet)
v1_router.register(r"genres", GenresViewSet)
v1_router.register(r"titles", TitleViewSet)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewsViewSet,
    basename="reviews",
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
