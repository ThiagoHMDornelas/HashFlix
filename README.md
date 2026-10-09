# HashFlix

> Projeto desenvolvido com base no curso **Hashtag Treinamentos**.

![Testes](https://github.com/ThiagoHMDornelas/HashFlix/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Django](https://img.shields.io/badge/django-5.2-092E20)
![License](https://img.shields.io/badge/license-MIT-green)

Clone de plataforma de streaming ("Netflix fake") desenvolvido com Django. Usuários se cadastram, fazem login e navegam por um catálogo de filmes organizado por categorias, com página de detalhes, episódios, contador de visualizações, histórico de "filmes vistos" e busca por título.

![Página inicial do HashFlix](docs/img/hashflix_home.png)

*Página inicial — apresentação da plataforma.*

## Sumário

- [Visão geral](#visão-geral)
- [Telas do projeto](#telas-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados](#banco-de-dados)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Principais rotas](#principais-rotas)
- [Painel administrativo](#painel-administrativo)
- [Licença](#licença)

## Visão geral

O **HashFlix** é uma aplicação web de streaming construída com Django (templates e Class-Based Views). Visitantes acessam a página inicial e criam conta; usuários autenticados navegam pelo catálogo de filmes, assistem aos detalhes, pesquisam títulos e editam o próprio perfil. Cada filme possui episódios e uma categoria, e o sistema registra quantas vezes cada filme foi visualizado e o histórico de filmes vistos por usuário. A interface usa Bootstrap 5 e Tailwind CSS, e os filmes (com thumbnails) são gerenciados pelo painel administrativo.

## Telas do projeto

**Catálogo de filmes** — destaque, seções "Novo", "Em Alta" e "Continuar Assistindo":

![Catálogo de filmes](docs/img/hashflix_catalog.png)

**Detalhes do filme** — informações, player de vídeo e filmes relacionados:

![Detalhes do filme](docs/img/hashflix_detail.png)

## Funcionalidades

- Cadastro, login e logout de usuários (usuário customizado `filme.Usuario`)
- Catálogo de filmes organizado por categorias
- Página de detalhes do filme com episódios e filmes relacionados
- Player de vídeo embutido (YouTube) com conversão automática das URLs dos episódios para o formato de embed
- Contador de visualizações por filme
- Histórico de "filmes vistos" por usuário ("Continuar Assistindo")
- Busca de filmes por título
- Edição de perfil e troca de senha
- Painel administrativo do Django com o histórico de filmes do usuário

## Tecnologias

- Python
- Django 5.2
- django-crispy-forms + crispy-bootstrap5
- python-dotenv e dj-database-url (variáveis de ambiente e banco)
- Pillow (upload de imagens)
- WhiteNoise (arquivos estáticos)
- SQLite e PostgreSQL
- Bootstrap 5 e Tailwind CSS (CDN)
- Docker e Docker Compose
- flake8 (desenvolvimento)
- GitHub Actions (CI)

## Estrutura do projeto

```
HashFlix/
├── hashflix/           # configurações do projeto (settings, urls, wsgi/asgi)
├── filme/              # app principal (models, views, forms, urls, admin, context processors)
├── templates/          # templates base e navbar
├── static/             # imagens de origem
├── media/              # thumbnails dos filmes
├── .github/workflows/  # pipeline de CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
├── .env.example        # exemplo de variáveis de ambiente
├── Procfile            # comando de start em produção (gunicorn)
├── runtime.txt         # versão do Python usada no deploy
├── manage.py
├── requirements.txt
└── requirements_dev.txt
```

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Crie o arquivo de ambiente (veja [Variáveis de ambiente](#variáveis-de-ambiente)):

    copy .env.example .env        # Windows
    cp .env.example .env          # Linux/macOS

Aplique as migrações:

    python manage.py migrate

Crie um usuário administrador:

    python manage.py createsuperuser

Inicie o servidor:

    python manage.py runserver

A aplicação estará disponível em:

    http://127.0.0.1:8000/

## Variáveis de ambiente

Copie o `.env.example` para `.env` e ajuste os valores:

    # Django
    SECRET_KEY=troque-por-uma-chave-secreta
    DEBUG=True
    ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost

    # Banco de dados (opcional): sem DATABASE_URL o projeto usa SQLite
    # DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hashflix

    # Superusuário criado automaticamente na inicialização (opcional)
    DJANGO_SUPERUSER_USERNAME=
    DJANGO_SUPERUSER_EMAIL=
    DJANGO_SUPERUSER_PASSWORD=

Se as três variáveis `DJANGO_SUPERUSER_*` forem preenchidas, um superusuário é criado automaticamente na inicialização (útil em deploys).

## Banco de dados

O projeto usa **SQLite** (`db.sqlite3`) por padrão. Para usar **PostgreSQL**, basta definir `DATABASE_URL` no `.env`:

    DATABASE_URL=postgresql://usuario:senha@host:5432/hashflix

A escolha é feita automaticamente: se `DATABASE_URL` existir, usa PostgreSQL (via `dj-database-url`); caso contrário, usa SQLite.

## Executar com Docker

A forma recomendada de rodar a aplicação. O Docker Compose sobe o serviço já configurado (Django + SQLite), sem precisar montar o ambiente Python manualmente.

**Pré-requisitos:**

- Docker Desktop instalado e em execução (engine)
- Docker Compose (já vem com o Docker Desktop)
- Git instalado (para clonar o repositório)
- A porta `8000` livre

> **Importante:** o Docker Desktop sozinho **não** faz o setup inicial — ele é o *engine* e o painel de gerenciamento. Clonar o repositório e rodar `docker compose up --build` são feitos pelo **terminal**; o Docker Desktop é ótimo para acompanhar logs, iniciar/parar e abrir um terminal dentro do container **depois** que a stack subiu.

> O Docker **não** precisa do arquivo `.env`: as variáveis já vêm definidas no `docker-compose.yml`. O `.env.example` é usado apenas na execução local (fora do Docker).

### Passo a passo (via shell / PowerShell)

**1. Clone o repositório**

```powershell
git clone https://github.com/ThiagoHMDornelas/HashFlix.git
cd HashFlix
```

> O `git clone` cria a pasta `HashFlix` dentro da pasta atual, e o `cd` entra nela. Se você **já está dentro** da pasta do projeto, **pule o `cd`**.

**2. Suba a stack.** Na primeira execução o Docker compila a imagem do projeto — pode levar alguns minutos:

```powershell
docker compose up --build -d
```

**3. Confira os containers:**

```powershell
docker compose ps
```

Espere o serviço `web` como `Up`.

| Serviço | Porta | Acesso |
|---|---|---|
| `web` | 8000 | `http://localhost:8000` |

**4. Acesse a aplicação:**

- Aplicação: `http://localhost:8000/`
- Painel administrativo: `http://localhost:8000/admin/`

As migrações são aplicadas automaticamente na inicialização.

**5. Crie o usuário administrador:**

```powershell
docker compose exec web python manage.py createsuperuser
```

> Para cadastrar filmes, use o painel administrativo (`/admin/`) — os filmes precisam de título, thumbnail e categoria.

**6. Comandos úteis:**

```powershell
docker compose logs -f web     # logs da aplicação
docker compose restart web     # reinicia a aplicação
docker compose down            # para e remove os containers
```

> O banco SQLite é criado dentro do container, então os dados **não persistem** após um `docker compose down`.

### Usando o Docker Desktop (interface gráfica)

Depois que a stack estiver no ar (passo 2), o Docker Desktop ajuda a operar. Na aba **Containers** você verá o serviço `web`:

- **Logs**: clique no container → aba *Logs* (equivale a `docker compose logs`).
- **Start / Stop / Restart**: botões no topo do container.
- **Terminal no container**: botão *Exec* (útil para depurar dentro do container).
- **Abrir no navegador**: clique na porta publicada (`8000:8000`).

O que **não** dá para fazer pela interface gráfica: clonar o repositório e rodar `docker compose up --build` em um clone novo (isso é feito pelo terminal).

### Problemas comuns

- **A aplicação não abre**
  - Veja os logs: `docker compose logs -f web`
  - Confirme que o container está `Up`: `docker compose ps`
- **Erro de porta em uso** (`8000`) → pare o serviço que ocupa a porta ou ajuste o mapeamento no `docker-compose.yml` (ex.: `8001:8000`) e acesse em `http://localhost:8001`
- **Os dados sumiram após reiniciar** → é esperado: o SQLite fica dentro do container e não persiste após um `docker compose down`

## Testes

A suíte de testes cobre models, formulários, views (incluindo autenticação e busca) e os context processors. Execute:

    python manage.py test

O **lint** do código é feito com `flake8` (configuração em `.flake8`):

    flake8

A suíte e o lint também rodam automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`), e o resultado é exibido no badge no topo deste README.

## Principais rotas

| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/` | Página inicial (formulário de e-mail) |
| GET | `/filmes/` | Catálogo de filmes (requer login) |
| GET | `/filmes/<id>` | Detalhes do filme (requer login) |
| GET | `/pesquisa/` | Busca de filmes por título (requer login) |
| GET/POST | `/criarconta/` | Cadastro de usuário |
| GET/POST | `/login/` | Login |
| POST | `/logout/` | Logout |
| GET/POST | `/editarperfil/<id>` | Edição do perfil (requer login) |
| GET/POST | `/mudarsenha/` | Troca de senha (requer login) |
| GET | `/admin/` | Painel administrativo |

## Painel administrativo

Acesse `/admin/` com o superusuário criado. Filmes, episódios e usuários ficam disponíveis para gerenciamento, e o histórico de filmes vistos aparece no cadastro do usuário.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
