from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from users_service.addresses.models import Address
from .serializers import AddressSerializer

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        address = serializer.save(user=self.request.user)

        if not Address.objects.filter(user=self.request.user).exclude(id=address.id).exists():
            address.is_default = True
            address.save()

    @action(detail=True, methods=["patch"])
    def set_default(self, request, pk=None):
        address = self.get_object()
        if address.user != request.user:
            return Response({"detail": "Não autorizado a alterar este endereço."}, status=status.HTTP_403_FORBIDDEN)

        address.is_default = True
        address.save()

        Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)

        return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
