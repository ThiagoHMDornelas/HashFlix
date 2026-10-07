from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'

    def ready(self):
        import os
        from django.db.utils import OperationalError, IntegrityError
        from .models import Usuario

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        # Só tenta criar se as variáveis existirem
        if username and email and password:
            try:
                # Verifica se já existe um superusuário com esse usuário
                if not Usuario.objects.filter(username=username).exists():
                    Usuario.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                    )
            except (OperationalError, IntegrityError):
                # Ignora se o banco ainda não estiver pronto ou se já existir
                pass
