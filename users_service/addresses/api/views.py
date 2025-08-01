from rest_framework.viewsets import ModelViewSet
from users_service.addresses.models import Address
from .serializers import AddressSerializer

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)