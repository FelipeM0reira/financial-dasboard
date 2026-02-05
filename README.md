# 📊 Budget Tracker - Gestão Financeira Pessoal

Uma aplicação fullstack de gestão financeira pessoal desenvolvida com metodologia TDD, demonstrando habilidades profissionais em React + Django.

> 📚 **Documentação completa disponível em:**
>
> - [📖 Estrutura Completa](./DOCUMENTACAO.md)

## 🎨 Screenshots

<div align="center">
  <div style="display: inline-block; margin: 0 5px; vertical-align: top;">
    <h4>Dashboard</h4>
    <img src="https://github.com/user-attachments/assets/2aa77685-75c2-4580-97b1-6324a0a24fb7" alt="Dashboard Screenshot" width="400px" style="border: 1px solid #ddd; border-radius: 5px;" />
  </div>

  <div style="display: inline-block; margin: 0 5px; vertical-align: top;">
    <h4>Transactions</h4>
    <img src="https://github.com/user-attachments/assets/ecaf0f6f-bab4-4162-b7d9-62c10b232a67" alt="Transactions Screenshot" width="400px" style="border: 1px solid #ddd; border-radius: 5px;" />
  </div>
</div> 


## 🛠️ Funcionalidades

### Autenticação Segura

- Registro com validação de senha forte
- Login com JWT (Access + Refresh tokens)
- Recuperação de senha via email
- Proteção de rotas

- https://github.com/user-attachments/assets/ae7823a8-3f43-4b00-a382-59d40e81a7bc

### Gestão de Transações

- CRUD completo (Criar, Listar, Editar, Deletar)
- Categorias: Alimentação, Transporte, Moradia, Saúde, Lazer, Educação, Salário, Investimentos, Outros
- Tipos: Receita e Despesa
- Filtros por mês, categoria e tipo
- Paginação

- https://github.com/user-attachments/assets/0a9caeee-12c2-4672-a3e2-1024d0670fdc

### Relatórios e Análises

- Dashboard com resumo mensal
- Gráficos de despesas por categoria
- Cálculo de saldo (receitas - despesas)
- Export para CSV

- https://github.com/user-attachments/assets/3996890c-98cb-47c0-b0bc-febe16442b29

## 💻 Tecnologias!

### Backend

- **Django 4.2** - Framework web Python
- **Django REST Framework** - API REST
- **SimpleJWT** - Autenticação JWT
- **PostgreSQL** - Banco de dados
- **pytest** - Testes automatizados (65 testes)

### Frontend

- **React 18** - Biblioteca UI
- **Vite** - Build tool
- **Tailwind CSS** - Estilização
- **Chart.js** - Gráficos
- **React Router** - Roteamento

### DevOps

- **Docker Compose** - Desenvolvimento local

## 📁 Estrutura do Projeto

Para documentação detalhada, veja [DOCUMENTACAO.md](./DOCUMENTACAO.md).

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

📖 **Para guia mais detalhado, veja [DOCUMENTACAO.md](./DOCUMENTACAO.md)**

### Rodar Testes

```bash
# Com Docker (recomendado)
docker-compose exec backend pytest -v

# Sem Docker (requer setup local)
cd backend && python -m venv venv
source venv/bin/activate
```

2. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
# Edite o arquivo .env se necessário
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

### Autenticação

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

### Filtros Disponíveis

- `?month=2024-01` - Filtrar por mês
- `?category=alimentacao` - Filtrar por categoria
- `?transaction_type=despesa` - Filtrar por tipos

## Seguranca

- Senhas hasheadas com PBKDF2
- Tokens JWT com expiração curta (5 min access, 24h refresh)
- Validação de senha forte (8+ caracteres, maiúscula, minúscula, número, especial)
- HTTPS obrigatório em produção
- CORS configurado para domínio específico
- Valores financeiros com DecimalField (precisão de 2 casas)

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

##👨‍💻 Autor

 [<img src="https://avatars.githubusercontent.com/u/104744113?v=4" width=115><br><sub>Felipe Moreira</sub>](https://github.com/FelipeM0reira) 

## Licenca

MIT.
