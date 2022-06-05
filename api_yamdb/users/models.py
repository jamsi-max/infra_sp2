from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class UserRole:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


ROLE = (
    (UserRole.USER, UserRole.USER),
    (UserRole.MODERATOR, UserRole.MODERATOR),
    (UserRole.ADMIN, UserRole.ADMIN),
)


class YamdbUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "info": ("Username уже используется."),
        },
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            "info": ("Email уже используется"),
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=len(max([max(i) for i in ROLE], key=len)),
        choices=ROLE,
        default=UserRole.USER,
    )
    bio = models.TextField("Биография", blank=True)

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_staf(self):
        return self.is_staf

    def __str__(self):
        return self.username
