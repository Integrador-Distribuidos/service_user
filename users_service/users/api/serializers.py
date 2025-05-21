from rest_framework import serializers

from users_service.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "city", "uf", "zip_code", "address", "type",]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
