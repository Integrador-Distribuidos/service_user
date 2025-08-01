from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  

    def validate(self, attrs):
        print("📥 Dados recebidos no backend:", attrs)

        email = attrs.get("email")
        password = attrs.get("password")

        if email is None or password is None:
            raise serializers.ValidationError(_("É necessário incluir 'email' e 'password'."))

        user = authenticate(self.context['request'], username=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Email ou senha inválidos."))

        if not user.is_active:
            raise serializers.ValidationError(_("Usuário está inativo."))

        self.user = user
        data = super().validate({self.username_field: email, "password": password})

        data.update({
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "type": user.type,
        })

        print("📤 Dados de retorno:", data)

        return data


    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["type"] = user.type
        return token

class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()
