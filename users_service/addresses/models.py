from django.db import models
from users_service.users.models import User

class Address(models.Model):
    user = models.ForeignKey(User, related_name="addresses" ,on_delete=models.CASCADE)
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=255, verbose_name="Número")
    neighborhood = models.CharField(max_length=255, verbose_name="Bairro")
    city = models.CharField(max_length=255, verbose_name="Cidade")
    state = models.CharField(max_length=255, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    uf = models.CharField(max_length=2, verbose_name="UF")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.street
