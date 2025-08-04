from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users_service.users.models import User
from .serializers import UserSerializer, UserCreateSerializer

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

        if user != request.user:
            return Response({"detail": "Você não pode modificar o tipo de outro usuário."}, status=status.HTTP_403_FORBIDDEN)

        if user.type != User.UserType.CLIENT:
            return Response({"detail": "Este usuário já é admin."}, status=status.HTTP_400_BAD_REQUEST)

        user.type = User.UserType.ADMIN
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
