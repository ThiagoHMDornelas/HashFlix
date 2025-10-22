from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'

    def ready(self):
        from .models import Usuario
        import os
        from django.db.utils import OperationalError, IntegrityError

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")

        # Só tenta criar se as variáveis existirem
        if email and senha:
            try:
                # Verifica se já existe um admin com esse e-mail
                if not Usuario.objects.filter(email=email).exists():
                    Usuario.objects.create_superuser(
                        username="admin",
                        email=email,
                        password=senha,
                        is_active=True,
                        is_staff=True,
                    )
            except (OperationalError, IntegrityError):
                # Ignora se o banco ainda não estiver pronto ou se já existir
                pass
