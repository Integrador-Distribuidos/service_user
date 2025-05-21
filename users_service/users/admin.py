from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User


if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informações pessoais"), {
            "fields": (
                "first_name",
                "last_name",
                "type",
                "city",
                "uf",
                "zip_code",
                "address",
            )
        }),
        (_("Permissões"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "type",
                "city",
                "uf",
                "zip_code",
                "address",
            ),
        }),
    )

    list_display = ["email", "first_name", "last_name", "type", "is_superuser"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ["id"]
