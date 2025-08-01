from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests
from users_service.users.models import User
from .serializers import CustomTokenObtainPairSerializer, GoogleAuthSerializer


# ========== USER DETAIL VIEW ==========

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"

user_detail_view = UserDetailView.as_view()


# ========== USER UPDATE VIEW ==========

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user

user_update_view = UserUpdateView.as_view()


# ========== USER REDIRECT VIEW ==========

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})

user_redirect_view = UserRedirectView.as_view()


# ========== JWT LOGIN ==========
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ========== GOOGLE LOGIN ==========

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("📥 Dados recebidos no Google Login:", request.data)

        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']

        google_user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        print("🔐 Token recebido do frontend:", access_token)

        try:
            response = requests.get(
                google_user_info_url,
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=5
            )
        except requests.RequestException as e:
            print("❌ Erro na requisição para Google:", str(e))
            return Response({'detail': 'Erro ao conectar com Google.'}, status=500)

        print("📡 Código de status do Google:", response.status_code)
        print("🧾 Conteúdo bruto:", response.text)

        if response.status_code != 200:
            return Response(
                {'detail': 'Token do Google inválido ou erro ao obter dados.', 'google_status': response.status_code},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_data = response.json()
        except ValueError:
            print("❌ Erro ao interpretar resposta da API do Google.")
            return Response({'detail': 'Erro ao interpretar resposta da API do Google.'}, status=500)

        print("👤 Dados do usuário do Google:", user_data)

        email = user_data.get('email')
        if not email:
            return Response({'detail': 'Email não encontrado nos dados do Google.'}, status=400)

        user, created = User.objects.get_or_create(email=email, defaults={
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'is_active': True,
        })

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
