from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get("email")
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email=email)
            print(f"User found: {user.email}")
        except UserModel.DoesNotExist:
            print("User does not exist.")
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            print("Password valid and user can authenticate.")
            return user
        else:
            print("Invalid password or user cannot authenticate.")
        return None

