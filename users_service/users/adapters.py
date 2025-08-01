from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import JsonResponse
from allauth.account.utils import user_email
import logging

logger = logging.getLogger(__name__)

class AccountAdapter(DefaultAccountAdapter):
    pass

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Este método é chamado antes do login social acontecer.
        Aqui, verificamos se o email do login social já existe.
        Se sim, conectamos o social account ao user existente.
        """
        email = user_email(sociallogin.user)
        
        if not email:
            logger.warning("Login social sem email.")
            return  

        user = self.get_user(email=email)

        if user:
            if user.is_active:
                logger.info(f"Usuário {user.email} já existe. Conectando ao login social.")
                sociallogin.connect(request, user)
            else:
                logger.error(f"Tentativa de login social com um usuário inativo: {user.email}")
                raise ImmediateHttpResponse(JsonResponse({"detail": "Usuário está inativo."}, status=400))
        else:
            logger.info(f"Nenhum usuário encontrado para o e-mail {email}. Criando novo usuário.")
            sociallogin.save(request)