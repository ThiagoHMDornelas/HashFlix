# AGENTS.md — HashFlix

Clone de plataforma de streaming ("Netflix fake") em Django: catálogo de filmes, autenticação e player de vídeos (YouTube embed). Django 5.2.1 · django-crispy-forms 2.4 + crispy-bootstrap5 · Whitenoise 6.11.0 · dj-database-url 3.0.1 · Pillow · gunicorn · SQLite ou PostgreSQL (`DATABASE_URL`) · Docker (porta 8000) · deploy em Railway.

## Contexto em camadas
`SOUL.md` (regras globais do agente) → `AGENTS.md` da pasta da linguagem (regras comuns) → este arquivo (particularidades do projeto). Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Arquitetura

- **Projeto de app único**: só existe o app `filme`; `hashflix/` é a configuração. Roteamento do app em `filme/urls.py` com `app_name = 'filme'` (sempre usar `reverse('filme:...')`).
- **`AUTH_USER_MODEL = "filme.Usuario"`**: `Usuario` é `AbstractUser` + `filmes_vistos` (M2M com `Filme`). Deve estar definido **antes** de qualquer migração.
- **Sem API REST**: full-stack Django com templates (`templates/` na raiz + `filme/templates/`), crispy-forms com template Bootstrap 5.
- **Middlewares extras**: `WhiteNoiseMiddleware` logo após o `SecurityMiddleware` (estáticos em produção); estáticos coletados em `staticfiles/`.

### Apps/módulos

| Módulo | Finalidade | Particularidades |
|---|---|---|
| `hashflix/` | Config | `settings.py` com lógica condicional de Railway (ver abaixo) |
| `filme/` | Models, views, templates do catálogo | Único app; migração inicial `0001_initial` |
| `templates/`, `static/`, `media/` | Assets e uploads | `thumb_filmes/` dentro de `media/` para thumbs |

### Modelos (`filme/models.py`)

- `Filme`: `titulo`, `thumb` (ImageField), `descricao` (1000), `categoria` (choices: Análises, Programação, Apresentação, Outros), `visualizacoes`, `data_criacao`.
- `Episodio`: FK `Filme` (`related_name="episodios"`), `video` URLField — `save()` **reescreve automaticamente** a URL via `converter_para_embed` (aceita `watch?v=`, `youtu.be`, `shorts`, `embed` → converte para `youtube.com/embed/<id>`; não-YouTube passa sem alteração).
- `Usuario`: ver acima.

## Comportamentos não óbvios

- **Superusuário automático**: `filme/apps.py` `ready()` cria superusuário no boot se `DJANGO_SUPERUSER_USERNAME`, `EMAIL` e `PASSWORD` estiverem definidos (silencia `OperationalError`/`IntegrityError` — não é comando, roda no import da app).
- **Contadores de visualização**: acessar `DetalhesFilme` incrementa `filme.visualizacoes` e adiciona ao `usuario.filmes_vistos` no `get()` da view (antes de renderizar).
- **Context processors** (`filme/novos_context.py`): toda página recebe `lista_filmes_recentes` + `lista_destaque` (8 últimos) e `lista_filmes_emalta` (8 mais vistos).
- **Perfil restrito ao dono**: `PaginaPerfil.dispatch` redireciona para o próprio perfil quando `pk` ≠ usuário logado.
- **Fluxo da homepage**: `FormHomepage` (só e-mail) → decide redirecionar para `login?username=...` ou `criarconta?email=...` com `from_homepage=true`.
- **Player YouTube**: `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'` evita o "Erro 153" do embed externo.

## Testes e lint

- Suíte obrigatória antes de entregar: **`python manage.py test`** (runner nativo do Django, `filme/tests.py`).
- Lint com flake8 (`.flake8`).
- CI (`.github/workflows/tests.yml`): com `SECRET_KEY`/`DEBUG` fake, roda `flake8` e então `python manage.py test` — Python 3.12.

## Banco de dados

- Sem `DATABASE_URL` (ou `DATABASE_PUBLIC_URL`) → SQLite (`db.sqlite3`).
- Com `DATABASE_URL` → `dj_database_url` com `conn_max_age=1800` (PostgreSQL via psycopg 3/2).
- Docker usa apenas SQLite (sem serviço de banco no compose).

## Variáveis de ambiente (.env.example)

`SECRET_KEY` (fallback: `TOKEN_CSRF` ou chave de desenvolvimento), `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL` (opcional), `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD` (opcional — superusuário no boot).

### Deploy no Railway

Definir `TOKEN_CSRF` ativa automaticamente o modo produção no settings: `CSRF_TRUSTED_ORIGINS`/`ALLOWED_HOSTS` apontam para `hashflix-production-98fb.up.railway.app` e `*.up.railway.app`. O `Procfile` faz `collectstatic --noinput` + `migrate` + `gunicorn hashflix.wsgi` (Python `3.13.7` no `runtime.txt`).

## Docker

Serviço único `web` (imagem `python:3.12-slim`, porta `8000`), que aplica migrações e sobe o servidor.

## Convenções

- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
