from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    signup_send_mail,
    get_token,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UsersViewSet,
)

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", signup_send_mail),
    path("v1/auth/token/", get_token),
]
