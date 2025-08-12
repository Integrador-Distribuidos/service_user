from rest_framework.exceptions import PermissionDenied, ValidationError
from users_service.users.models import User

class MakeAdminCommand:
    def __init__(self, user, requester):
        self.user = user
        self.requester = requester

    def execute(self):
        if self.user != self.requester:
            raise PermissionDenied("Você não pode modificar o tipo de outro usuário.")

        if self.user.type != User.UserType.CLIENT:
            raise ValidationError("Este usuário já é admin.")

        self.user.type = User.UserType.ADMIN
        self.user.save()
        return self.user
