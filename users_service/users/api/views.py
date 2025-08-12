from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users_service.users.models import User
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from .commands.make_admin_command import MakeAdminCommand
from .commands.update_cpf_command import UpdateCpfCommand


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAuthenticated])
    def make_admin(self, request, pk=None):
        user = self.get_object()
        
        try:
            command = MakeAdminCommand(user, request.user)
            updated_user = command.execute()
        except (PermissionDenied, ValidationError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAuthenticated])
    def update_cpf(self, request, pk=None):
        user = self.get_object()
        cpf = request.data.get("cpf")

        try:
            command = UpdateCpfCommand(user, cpf)
            updated_user = command.execute()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "CPF atualizado com sucesso!"}, status=status.HTTP_200_OK)
