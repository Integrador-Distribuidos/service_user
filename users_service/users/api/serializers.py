from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users_service.users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "city", "uf", "zip_code", "address", "type",]

        read_only_fields = ["id", "type"]

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "password", "city", "uf", "zip_code", "address"]
        
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            city=validated_data.get("city", ""),
            uf=validated_data.get("uf", ""),
            zip_code=validated_data.get("zip_code", ""),
            address=validated_data.get("address", ""),
            type=User.UserType.USER
        )
        return user