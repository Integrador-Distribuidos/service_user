
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for users_service.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    first_name = models.CharField(_("Nome"), max_length=150, blank=True)
    last_name = models.CharField(_("Sobrenome"), max_length=150, blank=True)
    cpf = models.CharField(_("CPF"), max_length=11, blank=True)
    email = models.EmailField(_("Email Address"), unique=True)
    username = None  # type: ignore[assignment]

    class UserType(models.TextChoices):
        CLIENT = "client", "Cliente"
        ADMIN = "admin", "Administrador"

    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENT,
        verbose_name="Tipo de Usuário"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def is_client(self) -> bool:
        return self.type == self.UserType.CLIENT

    @property
    def is_admin_system(self) -> bool:
        return self.type == self.UserType.ADMIN