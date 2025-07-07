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

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "cpf" ,"email", "password"]
        
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            cpf=validated_data.get("cpf", ""),
            type=User.UserType.CLIENT
        )
        return user