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

## 💻 Tecnologias!

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
- **React Router** - Roteamento

### DevOps

- **Docker Compose** - Desenvolvimento local

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
- `?transaction_type=despesa` - Filtrar por tipoS

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

## Autor

Desenvolvido por **Joao Felipe** como projeto de portfolio para demonstrar habilidades fullstack com React + Django.

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
