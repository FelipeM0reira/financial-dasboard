# Budget Tracker - Gestao Financeira Pessoal

Uma aplicacao fullstack de gestao financeira pessoal desenvolvida com metodologia TDD, demonstrando habilidades profissionais em React + Django.

## Screenshots

![Dashboard](https://via.placeholder.com/800x400/3b82f6/ffffff?text=Dashboard+Preview)
![Transactions](https://via.placeholder.com/800x400/22c55e/ffffff?text=Transactions+Preview)

## Tecnologias

### Backend
- **Django 4.2** - Framework web Python
- **Django REST Framework** - API REST
- **SimpleJWT** - Autenticacao JWT
- **PostgreSQL** - Banco de dados
- **pytest** - Testes automatizados (65 testes)

### Frontend
- **React 18** - Biblioteca UI
- **Vite** - Build tool
- **Tailwind CSS** - Estilizacao
- **Chart.js** - Graficos
- **Axios** - Cliente HTTP
- **React Router** - Roteamento

### DevOps
- **Docker Compose** - Desenvolvimento local
- **Render** - Deploy backend
- **Vercel** - Deploy frontend
- **Supabase** - Banco PostgreSQL (producao)

## Funcionalidades

### Autenticacao Segura
- Registro com validacao de senha forte
- Login com JWT (Access + Refresh tokens)
- Recuperacao de senha via email
- Protecao de rotas

### Gestao de Transacoes
- CRUD completo (Criar, Listar, Editar, Deletar)
- Categorias: Alimentacao, Transporte, Moradia, Saude, Lazer, Educacao, Salario, Investimentos, Outros
- Tipos: Receita e Despesa
- Filtros por mes, categoria e tipo
- Paginacao

### Relatorios e Analises
- Dashboard com resumo mensal
- Graficos de despesas por categoria
- Calculo de saldo (receitas - despesas)
- Export para CSV

## Estrutura do Projeto

```
financial_dashboard/
├── backend/
│   ├── core/                 # Configuracoes Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── authentication/       # App de autenticacao
│   │   ├── models.py         # CustomUser
│   │   ├── serializers.py    # Register, Login, PasswordReset
│   │   ├── views.py
│   │   └── tests/            # 28 testes
│   ├── transactions/         # App de transacoes
│   │   ├── models.py         # Transaction
│   │   ├── serializers.py
│   │   ├── views.py          # CRUD + Report + Export
│   │   ├── filters.py
│   │   └── tests/            # 37 testes
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/       # Button, Modal
│   │   │   ├── layout/       # Header
│   │   │   └── transactions/ # Form, Filters, Charts
│   │   ├── contexts/         # AuthContext, TransactionContext
│   │   ├── pages/            # Login, Register, Dashboard, Transactions
│   │   └── services/         # API client
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Como Rodar Localmente

### Pre-requisitos
- Docker e Docker Compose
- Git

### Passo a Passo

1. **Clone o repositorio**
```bash
git clone https://github.com/seu-usuario/budget-tracker.git
cd budget-tracker
```

2. **Configure as variaveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env se necessario
```

3. **Suba os containers**
```bash
docker-compose up --build
```

4. **Acesse a aplicacao**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Admin Django: http://localhost:8000/admin

### Rodar Testes (Backend)

```bash
# Com Docker
docker-compose exec backend pytest -v

# Sem Docker (ambiente virtual)
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pytest -v
```

## API Endpoints

### Autenticacao
| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/api/auth/register/` | Registrar usuario |
| POST | `/api/auth/login/` | Login (retorna tokens) |
| POST | `/api/auth/token/refresh/` | Renovar access token |
| POST | `/api/auth/password-reset/` | Solicitar reset de senha |
| POST | `/api/auth/password-reset/confirm/` | Confirmar nova senha |

### Transacoes
| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/api/transactions/` | Listar transacoes |
| POST | `/api/transactions/` | Criar transacao |
| GET | `/api/transactions/{id}/` | Detalhe da transacao |
| PUT | `/api/transactions/{id}/` | Atualizar transacao |
| DELETE | `/api/transactions/{id}/` | Deletar transacao |
| GET | `/api/transactions/report/` | Relatorio mensal |
| GET | `/api/transactions/export/` | Exportar CSV |

### Filtros Disponiveis
- `?month=2024-01` - Filtrar por mes
- `?category=alimentacao` - Filtrar por categoria
- `?transaction_type=despesa` - Filtrar por tipo

## Deploy

### Backend (Render)

1. Crie um projeto no [Render](https://render.com)
2. Conecte seu repositorio GitHub
3. Configure as variaveis de ambiente:
   - `SECRET_KEY` - Chave secreta Django
   - `DATABASE_URL` - URL do Supabase PostgreSQL
   - `CORS_ALLOWED_ORIGINS` - URL do frontend Vercel
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`

4. Deploy automatico a cada push na branch main

### Frontend (Vercel)

1. Crie um projeto no [Vercel](https://vercel.com)
2. Conecte seu repositorio GitHub
3. Configure a variavel de ambiente:
   - `VITE_API_URL` - URL do backend Render

4. Deploy automatico a cada push

### Banco de Dados (Supabase)

1. Crie um projeto no [Supabase](https://supabase.com)
2. Copie a connection string do PostgreSQL
3. Configure no Render como `DATABASE_URL`

## Limitacoes do Free Tier

> **Importante**: O plano gratuito do Render entra em "sleep" apos 15 minutos de inatividade. A primeira requisicao apos isso pode levar ~30 segundos (cold start). Em producao real, recomenda-se o plano pago para aplicacoes financeiras.

## Seguranca

- Senhas hasheadas com PBKDF2
- Tokens JWT com expiracao curta (5 min access, 24h refresh)
- Validacao de senha forte (8+ caracteres, maiuscula, minuscula, numero, especial)
- HTTPS obrigatorio em producao
- CORS configurado para dominio especifico
- Valores financeiros com DecimalField (precisao de 2 casas)

## Cobertura de Testes

```
======================= 65 passed in 7.53s ========================

authentication/tests/test_models.py      - 7 testes
authentication/tests/test_views.py       - 12 testes
authentication/tests/test_password_reset - 9 testes
transactions/tests/test_models.py        - 9 testes
transactions/tests/test_views.py         - 17 testes
transactions/tests/test_reports.py       - 11 testes
```

## Proximos Passos

- [ ] Two-Factor Authentication (2FA)
- [ ] Graficos de evolucao mensal
- [ ] Metas de economia
- [ ] Notificacoes de limites
- [ ] App mobile com React Native
- [ ] Integracao com Open Banking

## Autor

Desenvolvido por **Joao Gabriel** como projeto de portfolio para demonstrar habilidades fullstack com React + Django.

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
