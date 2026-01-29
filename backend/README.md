# 🔧 Backend - Documentação Técnica

## 📋 Índice

1. [Estrutura de Pastas](#estrutura-de-pastas)
2. [Apps Django](#apps-django)
3. [Modelos de Dados](#modelos-de-dados)
4. [Endpoints da API](#endpoints-da-api)
5. [Configurações](#configurações)
6. [Testes](#testes)
7. [Autenticação](#autenticação)
8. [Deployment](#deployment)

---

## 📁 Estrutura de Pastas

```
backend/
├── core/                    # Configurações centralizadas
│   ├── settings.py         # Todas as configs do Django
│   ├── urls.py             # URLs principais
│   └── wsgi.py             # WSGI app para produção
│
├── authentication/         # App de autenticação
│   ├── migrations/
│   ├── tests/
│   ├── models.py           # CustomUser model
│   ├── serializers.py      # Validação de dados
│   ├── views.py            # Endpoints
│   ├── urls.py             # Rotas
│   ├── admin.py            # Django admin
│   └── apps.py
│
├── transactions/           # App de transações
│   ├── migrations/
│   ├── tests/
│   ├── models.py           # Transaction model
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py          # Filtros customizados
│   ├── admin.py
│   └── apps.py
│
├── manage.py               # CLI Django
├── requirements.txt        # Dependências
├── Dockerfile              # Imagem Docker
├── entrypoint.sh           # Script de inicialização
└── pytest.ini              # Configuração de testes
```

---

## 🎯 Apps Django

### 1. Authentication App

#### **CustomUser Model**

```python
# backend/authentication/models.py

class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado que usa email em vez de username.
    """
    username = None                              # Remove campo username
    email = EmailField(unique=True)              # Email é único
    first_name = CharField(max_length=150)       # Nome (obrigatório)
    last_name = CharField(max_length=150)        # Sobrenome (opcional)

    USERNAME_FIELD = 'email'                     # Login com email
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()                # Manager customizado
```

**Como usar:**

```python
# Criar usuário
user = CustomUser.objects.create_user(
    email='usuario@exemplo.com',
    password='SenhaForte@123',
    first_name='João'
)

# Buscar por email
user = CustomUser.objects.get(email='usuario@exemplo.com')

# Validar senha
user.check_password('SenhaForte@123')  # True/False
```

#### **Serializers**

```python
# backend/authentication/serializers.py

class RegisterSerializer(serializers.ModelSerializer):
    """
    Validação de registro de novo usuário.

    Validações:
    - Email único
    - Senha forte (maiúscula, minúscula, número, caractere especial)
    - Mínimo 8 caracteres
    - Senhas coincidem
    """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customiza o serializador JWT para retornar dados do usuário.
    """
    username_field = 'email'  # Login com email

class PasswordResetRequestSerializer(serializers.Serializer):
    """Solicita reset de senha via email."""
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Confirma novo password com token."""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)
```

#### **Views (Endpoints)**

```python
# backend/authentication/views.py

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/

    Cria novo usuário. Qualquer pessoa pode acessar (AllowAny).

    Request:
    {
        "email": "usuario@exemplo.com",
        "first_name": "João",
        "last_name": "Silva",
        "password": "SenhaForte@123",
        "password_confirm": "SenhaForte@123"
    }

    Response (201):
    {
        "id": 1,
        "email": "usuario@exemplo.com",
        "first_name": "João",
        "last_name": "Silva",
        "message": "Usuário criado com sucesso!"
    }
    """

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/

    Autentica usuário e retorna tokens JWT.

    Request:
    {
        "email": "usuario@exemplo.com",
        "password": "SenhaForte@123"
    }

    Response (200):
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": 1,
            "email": "usuario@exemplo.com",
            "first_name": "João",
            "last_name": "Silva"
        }
    }
    """

class PasswordResetRequestView(APIView):
    """
    POST /api/auth/password-reset/

    Solicita reset de senha. Envia email com link seguro.

    Request:
    {
        "email": "usuario@exemplo.com"
    }

    Response (200):
    {
        "message": "Se o email existir em nossa base, você receberá..."
    }
    """

class PasswordResetConfirmView(APIView):
    """
    POST /api/auth/password-reset/confirm/

    Confirma reset de senha usando UID e token do email.

    Request:
    {
        "uid": "MQ==",
        "token": "abc123xyz",
        "new_password": "NovaSenha@456",
        "new_password_confirm": "NovaSenha@456"
    }

    Response (200):
    {
        "message": "Senha redefinida com sucesso!"
    }
    """
```

---

### 2. Transactions App

#### **Transaction Model**

```python
# backend/transactions/models.py

class Transaction(models.Model):
    """
    Modelo de transação (receita ou despesa).
    """
    CATEGORY_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('saude', 'Saúde'),
        ('lazer', 'Lazer'),
        ('educacao', 'Educação'),
        ('salario', 'Salário'),
        ('investimentos', 'Investimentos'),
        ('outros', 'Outros'),
    ]

    TYPE_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    user = ForeignKey(CustomUser, on_delete=CASCADE)
    description = CharField(max_length=255)
    amount = DecimalField(max_digits=10, decimal_places=2)
    category = CharField(choices=CATEGORY_CHOICES)
    type = CharField(choices=TYPE_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Como usar:**

```python
# Criar transação
transaction = Transaction.objects.create(
    user=user,
    description='Supermercado',
    amount=50.00,
    category='alimentacao',
    type='despesa'
)

# Listar transações do usuário
transactions = Transaction.objects.filter(user=user)

# Filtrar por categoria
food_expenses = transactions.filter(category='alimentacao')

# Filtrar por mês
from django.utils import timezone
current_month = timezone.now().month
transactions.filter(created_at__month=current_month)
```

#### **Serializers**

```python
# backend/transactions/serializers.py

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializa transações completas.
    """
    class Meta:
        model = Transaction
        fields = ('id', 'description', 'amount', 'category', 'type', 'created_at')
        read_only_fields = ('id', 'created_at')
```

#### **Views (Endpoints)**

```python
# backend/transactions/views.py

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Gerencia CRUD completo de transações.

    Endpoints:
    GET    /api/transactions/           - Listar (com filtros)
    POST   /api/transactions/           - Criar
    GET    /api/transactions/{id}/      - Detalhe
    PUT    /api/transactions/{id}/      - Atualizar (completo)
    PATCH  /api/transactions/{id}/      - Atualizar (parcial)
    DELETE /api/transactions/{id}/      - Deletar
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        """Retorna apenas transações do usuário logado."""
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Associa transação ao usuário logado."""
        serializer.save(user=self.request.user)
```

---

## 📊 Modelos de Dados

### Diagrama ER

```
┌─────────────────────────────────────┐
│         CustomUser                  │
├─────────────────────────────────────┤
│ id (PK)                             │
│ email (UNIQUE)                      │
│ first_name                          │
│ last_name                           │
│ password                            │
│ is_active                           │
│ is_staff                            │
│ date_joined                         │
└─────────────────────────────────────┘
         ▲                      │
         │                      │ 1:N (um usuário, muitas transações)
         │                      │
         │                      ▼
         │      ┌─────────────────────────────────────┐
         │      │      Transaction                    │
         │      ├─────────────────────────────────────┤
         │      │ id (PK)                             │
         │      │ user_id (FK) ─────────────┐         │
         │      │ description                         │
         │      │ amount                              │
         │      │ category                            │
         │      │ type (RECEITA/DESPESA)              │
         │      │ created_at                          │
         │      │ updated_at                          │
         │      └─────────────────────────────────────┘
```

---

## 🔌 Endpoints da API

### Autenticação

| Método | Endpoint                            | Descrição                |
| ------ | ----------------------------------- | ------------------------ |
| POST   | `/api/auth/register/`               | Registrar novo usuário   |
| POST   | `/api/auth/login/`                  | Login e obter tokens     |
| POST   | `/api/auth/token/refresh/`          | Renovar access token     |
| POST   | `/api/auth/password-reset/`         | Solicitar reset de senha |
| POST   | `/api/auth/password-reset/confirm/` | Confirmar nova senha     |

### Transações

| Método | Endpoint                  | Descrição                       |
| ------ | ------------------------- | ------------------------------- |
| GET    | `/api/transactions/`      | Listar transações (com filtros) |
| POST   | `/api/transactions/`      | Criar transação                 |
| GET    | `/api/transactions/{id}/` | Obter transação específica      |
| PUT    | `/api/transactions/{id}/` | Atualizar transação             |
| DELETE | `/api/transactions/{id}/` | Deletar transação               |

### Filtros

```
GET /api/transactions/?category=alimentacao&type=despesa&ordering=-created_at

Parâmetros:
- category: alimentacao, transporte, moradia, saude, lazer, educacao, salario, investimentos, outros
- type: receita, despesa
- ordering: created_at, -created_at, amount, -amount
```

---

## ⚙️ Configurações

### `backend/core/settings.py`

```python
# Banco de dados (PostgreSQL em produção, SQLite em testes)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'budget_tracker'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# JWT Tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=1440),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS - Permite requisições do frontend
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

## 🧪 Testes

### Estrutura de Testes

```
authentication/
  tests/
    __init__.py
    test_models.py         # Testa CustomUser model
    test_views.py          # Testa endpoints de autenticação
    test_password_reset.py # Testa reset de senha

transactions/
  tests/
    __init__.py
    test_models.py         # Testa Transaction model
    test_views.py          # Testa endpoints de transações
    test_reports.py        # Testa relatórios
```

### Executar Testes

```bash
# Todos os testes
docker-compose exec backend pytest

# Testes específicos
docker-compose exec backend pytest authentication/tests/test_views.py

# Com coverage
docker-compose exec backend pytest --cov=authentication --cov=transactions

# Verbose
docker-compose exec backend pytest -v
```

---

## 🔐 Autenticação

### Fluxo JWT

```
1. Registro
   POST /api/auth/register/
   ↓
   Cria usuário no banco

2. Login
   POST /api/auth/login/ (email, password)
   ↓
   Valida credenciais
   ↓
   Gera tokens JWT:
   - access_token (5 min)
   - refresh_token (24h)

3. Requisições Autenticadas
   GET /api/transactions/
   Header: Authorization: Bearer <access_token>
   ↓
   Backend valida token

4. Token Expirou
   POST /api/auth/token/refresh/ (refresh_token)
   ↓
   Gera novo access_token

5. Refresh token expirou
   POST /api/auth/login/ (novo login)
```

### Headers Obrigatórios

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json
```

---

## 🚀 Deployment

### Render (Backend)

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Build command: `python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command: `gunicorn core.wsgi`

### Variáveis de Ambiente

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta
DATABASE_URL=postgresql://user:pass@host/db
FRONTEND_URL=https://seu-frontend.com
CORS_ALLOWED_ORIGINS=https://seu-frontend.com
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

---

## 📚 Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/docs/)

---

**Desenvolvido com ❤️**
