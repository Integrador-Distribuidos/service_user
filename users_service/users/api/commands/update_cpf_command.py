from rest_framework.exceptions import ValidationError

class UpdateCpfCommand:
    def __init__(self, user, cpf):
        self.user = user
        self.cpf = cpf

    def execute(self):
        if self.user.cpf:
            raise ValidationError("CPF já preenchido.")

        if len(self.cpf) != 11:
            raise ValidationError("CPF inválido.")
        
        # Lógica de atualização do CPF
        self.user.cpf = self.cpf
        self.user.save()
        return self.user
