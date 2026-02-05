# 📊 Financial Dashboard - Documentação Completa

## 🎯 Visão Geral do Projeto

**Financial Dashboard** é uma aplicação web full-stack para gerenciamento de finanças pessoais. Permite que usuários registrem, categorizem e analisem suas receitas e despesas através de uma interface intuitiva com gráficos e relatórios.

---

## 🏗️ Arquitetura do Projeto

```
financial_dashboard/
├── backend/                    # Django REST API
│   ├── core/                   # Configurações do Django
│   ├── authentication/         # Autenticação e autorização
│   ├── transactions/           # Lógica de transações
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── entrypoint.sh
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── components/         # Componentes reutilizáveis
│   │   ├── contexts/           # Context API (Auth, Transactions)
│   │   ├── pages/              # Páginas principais
│   │   ├── services/           # API client
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── tailwind.config.js
├── docker-compose.yml          # Orquestração de containers
└── README.md
```

---

## 🛠️ Stack Tecnológico

### Frontend

- **React 18** - Biblioteca UI
- **Vite** - Build tool e dev server
- **React Router** - Navegação
- **Tailwind CSS** - Estilização
- **React Hot Toast** - Notificações
- **Axios** - Cliente HTTP

### Backend

- **Django 4.x** - Framework web
- **Django REST Framework** - APIs REST
- **PostgreSQL** - Banco de dados
- **Gunicorn** - WSGI server
- **Python 3.9+**

### DevOps

- **Docker** - Containerização
- **Docker Compose** - Orquestração local
- **PostgreSQL 15** - Database

---

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### Iniciar o Projeto

```bash
# Clone o repositório
git clone <repo-url>
cd financial_dashboard

# Inicie todos os containers
docker-compose up -d

# Acesse a aplicação
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

### Parar o Projeto

```bash
docker-compose down
```

---

## 📋 Funcionalidades Principais

### 1. **Autenticação**

- Registro de novos usuários
- Login com email e senha
- Recuperação de senha por email
- Reset de senha via link

- https://github.com/user-attachments/assets/05502edf-c1b0-4b49-b282-e56bbf952865

### 2. **Gerenciamento de Transações**

- Criar receitas e despesas
- Editar transações existentes
- Deletar transações
- Filtrar por período, categoria e tipo

- https://github.com/user-attachments/assets/5d4b3b32-723a-4a07-81f1-4cc53b2c77e7

### 3. **Análises e Relatórios**

- **Dashboard com resumo**: Total de receitas, despesas e saldo
- **Gráfico de Categorias**: Pizza chart mostrando distribuição por categoria
- **Tendência Mensal**: Gráfico de barras últimos 6 meses
- **Transações Recentes**: Lista das últimas 5 transações
- **Exportação CSV**: Baixar dados das transações

### 4. **Interface Responsiva**

- Layout adaptável para mobile, tablet e desktop
- Componentes reutilizáveis
- Navegação intuitiva

---

## 🔑 Credenciais de Desenvolvimento

O banco de dados está pré-configurado com:

- **Database**: budget_tracker
- **User**: postgres
- **Password**: postgres
- **Host**: db (container)
- **Port**: 5432

---

## 📱 Páginas da Aplicação

| Página          | Rota                          | Descrição                |
| --------------- | ----------------------------- | ------------------------ |
| Login           | `/`                           | Autenticação de usuários |
| Registro        | `/register`                   | Criação de nova conta    |
| Forgot Password | `/forgot-password`            | Solicitação de reset     |
| Reset Password  | `/reset-password/:uid/:token` | Reset via link           |
| Dashboard       | `/dashboard`                  | Resumo e análises        |
| Transações      | `/transactions`               | Gerenciamento completo   |

---

## 🔌 API Endpoints (Backend)

### Autenticação

```
POST   /auth/register/           # Registrar novo usuário
POST   /auth/login/              # Login
GET    /auth/user/               # Dados do usuário autenticado
POST   /auth/password-reset/     # Solicitar reset de senha
POST   /auth/password-reset/confirm/  # Confirmar novo password
```

### Transações

```
GET    /transactions/            # Listar transações
POST   /transactions/            # Criar transação
GET    /transactions/{id}/       # Detalhes da transação
PUT    /transactions/{id}/       # Atualizar transação
DELETE /transactions/{id}/       # Deletar transação
GET    /transactions/report/     # Relatório mensal
GET    /transactions/export/     # Exportar CSV
```

---

## 🎨 Componentes Frontend

### Páginas (pages/)

- `Login.jsx` - Formulário de login
- `Register.jsx` - Formulário de registro
- `Dashboard.jsx` - Painel principal com gráficos
- `Transactions.jsx` - Gerenciador de transações
- `ForgotPassword.jsx` - Solicitar reset
- `ResetPassword.jsx` - Confirmar novo password

### Componentes (components/)

- `SummaryCards.jsx` - Resumo financeiro
- `CategoryChart.jsx` - Gráfico de categorias
- `MonthlyTrend.jsx` - Gráfico de tendências mensais
- `TransactionForm.jsx` - Formulário de transação
- `TransactionFilters.jsx` - Filtros avançados

### Contextos (contexts/)

- `AuthContext.jsx` - Gerenciamento de autenticação
- `TransactionContext.jsx` - Gerenciamento de transações

---

## 🔒 Segurança

### Backend

- JWT tokens com expiração
- CORS configurado para frontend
- Validação de entrada em todos os endpoints
- Senhas hashadas com bcrypt
- Proteção contra CSRF

### Frontend

- Tokens armazenados em localStorage
- Rotas protegidas por autenticação
- Tratamento de erros de API
- Sanitização de inputs

---

## 📊 Modelos de Dados

### User (Django Auth)

```python
- id (PK)
- email
- password (hashed)
- first_name
- last_name
- created_at
```

### Transaction

```python
- id (PK)
- user (FK)
- description
- amount (Decimal)
- category
- transaction_type (receita/despesa)
- date
- created_at
- updated_at
```

### Recurring Transaction

```python
- id (PK)
- user (FK)
- base_transaction (FK)
- recurrence_pattern (mensal/semanal/diário)
- end_date
- active (Boolean)
```

---

## ⚙️ Variáveis de Ambiente

### Backend (.env)

```
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DB_NAME=budget_tracker
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000/api
```

---

## 🧪 Testes

### Backend

Execute testes com pytest:

```bash
# Dentro do container backend
docker-compose exec backend pytest
```

### Frontend

```bash
# Install dependencies
npm install

# Run tests
npm test
```

## 🤝 Contribuindo

Este é um projeto pessoal e para uso no meu portfólio. Sugestões de melhorias são bem-vindas.

---

## 📄 Licença

MIT

---

## 📧 Contato

Para dúvidas sobre o projeto, entre em contato através do repositório.

---

**Última atualização**: 04/02/2026
