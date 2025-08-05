# Stock2Sell - Serviço de usuários

users service

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Preencher os arquivos em .envs/.local/.django e .envs/.local/.postgres
```
.django:
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=True
DATABASE_URL=postgres://usuario_banco:senha_banco@postgres:5432/users

.postgres:
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

3. Buildar o projeto:
```
docker-compose -f docker-compose.local.yml up --build
```

4. Comandos adicionais:
```
| Ação                          | Comando                                                                                           |
| ----------------------------- | --------------------------------------------------------------------------------------------------|
| Fazer as migrações            | `docker-compose -f docker-compose.local.yml exec django python manage.py migrate`                 |
| Criar as migrações de um app  | `docker-compose -f docker-compose.local.yml exec django python manage.py makemigrations`          |
| Criar superusuário            | `docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser`         |
| Acessar o shell do Django     | `docker-compose -f docker-compose.local.yml exec django python manage.py shell`                   |
| Acessar terminal do container | `docker-compose -f docker-compose.local.yml exec django bash`                                     |
```


