# AGENTS.md — HashFlix

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
Clone de plataforma de streaming ("Netflix fake") em Django: catálogo de filmes, autenticação e upload de mídia.

**Stack:** Django 5.2.1 · django-crispy-forms + Bootstrap 5 · Whitenoise · dj-database-url · Pillow · gunicorn · Python 3.12 · SQLite ou PostgreSQL · Docker · Heroku (Procfile)

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `hashflix/` — projeto Django (`hashflix/settings.py`)
- `filme/` — app principal (modelos, views, templates)
- `templates/`, `static/`, `media/` — assets e uploads
- `Procfile`, `runtime.txt` — deploy Heroku
- `manage.py` na raiz

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Testes e lint
```bash
python manage.py test
flake8
```

## Particularidades
- Banco: sem `DATABASE_URL` usa SQLite (`db.sqlite3`); com `DATABASE_URL` usa PostgreSQL.
- Superusuário pode ser criado automaticamente na inicialização via `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD`.
- Arquivos enviados vão para `media/`; estáticos são servidos por Whitenoise em produção.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
