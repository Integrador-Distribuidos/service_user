from rest_framework.serializers import ModelSerializer,ValidationError
from rest_framework import serializers

from users_service.users.models import User


class UserSerializer(ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "cpf" ,"email", "type",]

        read_only_fields = ["id", "type"]

    def validate_email(self, value):
        user = self.instance
        if user and User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Esse email já está sendo usado por outro usuário.")
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "cpf", "email", "password", "password2"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            cpf=validated_data.get("cpf", ""),
            type=User.UserType.CLIENT,
        )
        return user
