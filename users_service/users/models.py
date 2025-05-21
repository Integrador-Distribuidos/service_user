
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
    email = models.EmailField(_("Email Address"), unique=True)
    city = models.CharField(_("Cidade"), max_length=100, blank=True)
    uf = models.CharField(_("Estado"), max_length=2, blank=True)
    zip_code = models.CharField(_("CEP"), max_length=8, blank=True)
    address = models.CharField(_("Endereço"), max_length=255, blank=True)
    username = None  # type: ignore[assignment]

    class UserType(models.TextChoices):
        USER = "user", "Usuário Comum"
        SELLER = "seller", "Vendedor"
        ADMIN = "admin", "Administrador"

    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.USER,
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
        return self.type == self.UserType.USER

    @property
    def is_seller(self) -> bool:
        return self.type == self.UserType.SELLER

    @property
    def is_admin_system(self) -> bool:
        return self.type == self.UserType.ADMIN