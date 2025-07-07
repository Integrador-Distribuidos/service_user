from rest_framework import serializers
from addresses.models import Address

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "number",
            "neighborhood",
            "city",
            "uf",
            "zip_code",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        # Preenche o campo user automaticamente com o usuário logado
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Preenche o campo user automaticamente com o usuário logado
        validated_data["user"] = self.context["request"].user
        return super().update(instance, validated_data)
    
