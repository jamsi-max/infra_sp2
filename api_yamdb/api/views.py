from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from django_filters import FilterSet, CharFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action, api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from .permissions import (
    IfUserIsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleReadSerializer,
    TitleSerializer,
    UserSerializer,
)

User = get_user_model()


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def signup_send_mail(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    try:
        user, _ = User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        return Response(
            {"info": "Usrname или email уже используются!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    comfirm_token = RefreshToken.for_user(user)
    send_mail(
        "Подтверждение регистрации на Yambd",
        f"Ваш код подтверждения {comfirm_token}",
        'support@yatub.com',
        [
            user.email,
        ],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = User.objects.get(username=serializer.validated_data["username"])
    except ObjectDoesNotExist:
        return Response(
            {"error": "Пользователь не существует!"},
            status=status.HTTP_404_NOT_FOUND,
        )
    try:
        payload = RefreshToken(serializer.validated_data["confirmation_code"])
        user_id = payload.get("user_id", None)
    except TokenError:
        return Response(
            {"error": "Токен не действительный или не существует!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user.id != user_id:
        return Response(
            {"error": "Username не соответствует токену!"},
            status=status.HTTP_404_NOT_FOUND,
        )
    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IfUserIsAdmin]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def me(self, request):
        if request.method == "GET":
            user = get_object_or_404(
                self.queryset, username=request.user.username
            )
            serializer = self.get_serializer(user, partial=False)
            return Response(serializer.data)

        user = get_object_or_404(
            self.queryset, username=request.user.username
        )
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    search_fields = ("name", "slug")


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name", "slug")
    lookup_field = "slug"


class TitleFilter(FilterSet):
    genre = CharFilter(field_name="genre__slug")
    category = CharFilter(field_name="category__slug")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ["category", "year", "genre", "name"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrAdminOrModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review_set = title.reviews.all()
        return review_set

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))

        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrAdminOrModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        return serializer.save(author=self.request.user, review=review)
