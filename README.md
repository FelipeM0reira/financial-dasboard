# 📊 Budget Tracker - Gestão Financeira Pessoal

Uma aplicação fullstack de gestão financeira pessoal desenvolvida com metodologia TDD, demonstrando habilidades profissionais em React + Django.

> 📚 **Documentação completa disponível em:**
>
> - [📖 Estrutura Completa](./DOCUMENTACAO_ESTRUTURA.md)
> - [⚡ Guia Rápido](./GUIA_RAPIDO.md)
> - [🔧 Backend](./backend/README.md)
> - [⚛️ Frontend](./frontend/README.md)
> - [🏗️ Arquitetura](./ARQUITETURA.md)
> - [✅ Checklist](./CHECKLIST_DESENVOLVIMENTO.md)

## 🎨 Screenshots

![Dashboard](https://via.placeholder.com/800x400/3b82f6/ffffff?text=Dashboard+Preview)
![Transactions](https://via.placeholder.com/800x400/22c55e/ffffff?text=Transactions+Preview)

## 💻 Tecnologias

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

## 📁 Estrutura do Projeto

Para documentação detalhada, veja [DOCUMENTACAO_ESTRUTURA.md](./DOCUMENTACAO_ESTRUTURA.md).

````
financial_dashboard/
├── backend/                          # Django REST API
│   ├── core/                         # Configurações
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # URLs principais
│   │   └── wsgi.py                  # WSGI app
│   ├── authentication/              # App de autenticação
│   │   ├── migrations/              # Migrações do BD
│   │   ├── tests/                   # 28 testes
│   │   ├── models.py                # CustomUser model
│   │   ├── serializers.py           # Validação
│   │   ├── views.py                 # Endpoints
│   │   └── urls.py                  # Rotas
│   ├── transactions/                # App de transações
│   │   ├── migrations/              # Migrações do BD
│   │   ├── tests/                   # 37 testes
│   │   ├── models.py                # Transaction model
│   │   ├── serializers.py           # Validação
│   │   ├── views.py                 # CRUD endpoints
│   │   ├── filters.py               # Filtros customizados
│   │   └── urls.py                  # Rotas
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── entrypoint.sh               # Script inicialização
│   └── README.md                    # Docs do backend
│
├── frontend/                        # React + Vite
│   ├── src/
│   │   ├── components/              # Componentes reutilizáveis
│   │   │   ├── common/             # Button, Input, Card, Modal
│   │   │   ├── layout/             # Header, Sidebar, Footer
│   │   │   └── transactions/       # TransactionForm, List, Filter
│   │   ├── contexts/               # Estado global
│   │   │   ├── AuthContext.jsx     # Autenticação
│  🚀 Como Começar

### Pré-requisitos

- ✅ Docker & Docker Compose
- ✅ Git

**Para desenvolvimento sem Docker (opcional):**
- Python 3.11+
- Node.js 18+

### Setup Rápido

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/financial_dashboard.git
cd financial_dashboard

# 2. Configure variáveis de ambiente
cp .env.example .env

# 3. Inicie os containers
docker-compose up --build

# 4. Acesse a aplicação
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/api
# Admin:    http://localhost:8000/admin
````

📖 **Para guia mais detalhado, veja [GUIA_RAPIDO.md](./GUIA_RAPIDO.md)**

### Rodar Testes

```bash
# Com Docker (recomendado)
docker-compose exec backend pytest -v

# Sem Docker (requer setup local)
cd backend && python -m venv venv
source venv/bin/activate
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

| Metodo | Endpoint                            | Descricao                |
| ------ | ----------------------------------- | ------------------------ |
| POST   | `/api/auth/register/`               | Registrar usuario        |
| POST   | `/api/auth/login/`                  | Login (retorna tokens)   |
| POST   | `/api/auth/token/refresh/`          | Renovar access token     |
| POST   | `/api/auth/password-reset/`         | Solicitar reset de senha |
| POST   | `/api/auth/password-reset/confirm/` | Confirmar nova senha     |

### Transacoes

| Metodo | Endpoint                    | Descricao            |
| ------ | --------------------------- | -------------------- |
| GET    | `/api/transactions/`        | Listar transacoes    |
| POST   | `/api/transactions/`        | Criar transacao      |
| GET    | `/api/transactions/{id}/`   | Detalhe da transacao |
| PUT    | `/api/transactions/{id}/`   | Atualizar transacao  |
| DELETE | `/api/transactions/{id}/`   | Deletar transacao    |
| GET    | `/api/transactions/report/` | Relatorio mensal     |
| GET    | `/api/transactions/export/` | Exportar CSV         |

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
