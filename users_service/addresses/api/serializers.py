from rest_framework import serializers
from users_service.addresses.models import Address

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
            "is_default",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):

        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data["user"] = self.context["request"].user
        return super().update(instance, validated_data)
