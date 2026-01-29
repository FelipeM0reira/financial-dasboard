# ⚛️ Frontend - Documentação Técnica

## 📋 Índice

1. [Estrutura de Pastas](#estrutura-de-pastas)
2. [Arquitetura](#arquitetura)
3. [Componentes](#componentes)
4. [Contexts (Estado Global)](#contexts-estado-global)
5. [Services (APIs)](#services-apis)
6. [Páginas](#páginas)
7. [Fluxos de Dados](#fluxos-de-dados)
8. [Deployment](#deployment)

---

## 📁 Estrutura de Pastas

```
frontend/src/
├── main.jsx                    # Entrada da aplicação
├── App.jsx                     # Componente raiz
├── index.css                   # Estilos globais
│
├── components/                 # Componentes reutilizáveis
│   ├── common/                 # Componentes genéricos
│   │   ├── Button.jsx         # Botão estilizado
│   │   ├── Input.jsx          # Campo de entrada
│   │   ├── Card.jsx           # Container card
│   │   ├── Modal.jsx          # Modal dialog
│   │   └── Toast.jsx          # Notificações
│   │
│   ├── layout/                 # Componentes de layout
│   │   ├── Header.jsx         # Barra superior
│   │   ├── Sidebar.jsx        # Menu lateral
│   │   ├── Footer.jsx         # Rodapé
│   │   └── MainLayout.jsx     # Layout principal
│   │
│   └── transactions/           # Componentes de transações
│       ├── TransactionForm.jsx
│       ├── TransactionList.jsx
│       ├── TransactionCard.jsx
│       └── TransactionFilter.jsx
│
├── pages/                      # Páginas completas
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── ForgotPassword.jsx
│   ├── ResetPassword.jsx
│   ├── Dashboard.jsx
│   └── Transactions.jsx
│
├── contexts/                   # Context API (Estado global)
│   ├── AuthContext.jsx
│   └── TransactionContext.jsx
│
└── services/                   # APIs e utilitários
    ├── api.js                  # Cliente Axios
    ├── auth.js                 # Funções de autenticação
    ├── transactions.js         # Funções de transações
    └── storage.js              # Gerenciamento localStorage
```

---

## 🏗️ Arquitetura

### Fluxo de Dados

```
User Input (formulário, clique)
         ↓
Component Handler
         ↓
Service Function (api.js, auth.js)
         ↓
API Backend
         ↓
Context Update (AuthContext, TransactionContext)
         ↓
Component Re-render
         ↓
UI Updated
```

### Stack

```
React 18
├── React Router (Navegação)
├── Vite (Build Tool)
├── Tailwind CSS (Estilização)
├── Axios (HTTP Client)
├── React Hot Toast (Notificações)
└── Chart.js (Gráficos)
```

---

## 🧩 Componentes

### Common Components

#### **Button.jsx**

```jsx
<Button
  onClick={handleClick}
  variant="primary" // primary, secondary, danger
  size="md" // sm, md, lg
  disabled={false}
  loading={false}
>
  Clique aqui
</Button>
```

#### **Input.jsx**

```jsx
<Input
  type="text"
  placeholder="Email"
  value={email}
  onChange={e => setEmail(e.target.value)}
  error={errors.email}
  required
/>
```

#### **Card.jsx**

```jsx
<Card>
  <Card.Header>Título</Card.Header>
  <Card.Body>Conteúdo</Card.Body>
  <Card.Footer>Rodapé</Card.Footer>
</Card>
```

#### **Modal.jsx**

```jsx
<Modal isOpen={isOpen} onClose={handleClose}>
  <Modal.Header>Título</Modal.Header>
  <Modal.Body>Conteúdo</Modal.Body>
  <Modal.Footer>
    <Button onClick={handleClose}>Cancelar</Button>
    <Button onClick={handleConfirm}>Confirmar</Button>
  </Modal.Footer>
</Modal>
```

#### **Toast.jsx (react-hot-toast)**

```jsx
import { toast } from 'react-hot-toast'

// Sucesso
toast.success('Operação realizada!')

// Erro
toast.error('Erro na operação')

// Loading
const toastId = toast.loading('Carregando...')
toast.success('Pronto!', { id: toastId })
```

### Layout Components

#### **MainLayout.jsx**

```jsx
// Componente que envolve todas as páginas
<MainLayout>
  <Header />
  <div className="flex">
    <Sidebar />
    <main className="flex-1">{children}</main>
  </div>
  <Footer />
</MainLayout>
```

#### **Header.jsx**

```jsx
// Barra superior
// - Logo
// - Menu de navegação
// - Usuário (nome, foto)
// - Logout button
```

#### **Sidebar.jsx**

```jsx
// Menu lateral
// - Links para Dashboard
// - Links para Transações
// - Links para Perfil
// - Tema (claro/escuro)
```

### Transaction Components

#### **TransactionForm.jsx**

```jsx
// Formulário criar/editar transação
<TransactionForm
  initialData={transaction} // null para criar, objeto para editar
  onSubmit={handleSubmit}
  onCancel={handleCancel}
/>
```

#### **TransactionList.jsx**

```jsx
// Lista com paginação
<TransactionList
  transactions={transactions}
  onEdit={handleEdit}
  onDelete={handleDelete}
  page={page}
  pageSize={pageSize}
  total={total}
/>
```

#### **TransactionCard.jsx**

```jsx
// Card individual de transação
<TransactionCard
  transaction={transaction}
  onEdit={() => {}}
  onDelete={() => {}}
/>
```

#### **TransactionFilter.jsx**

```jsx
// Filtros
<TransactionFilter
  filters={filters}
  onFilterChange={handleFilterChange}
  categories={categories}
/>
```

---

## 🎣 Contexts (Estado Global)

### AuthContext.jsx

```jsx
/**
 * Gerencia estado de autenticação da aplicação.
 *
 * Estado:
 * - user: Dados do usuário logado
 * - isAuthenticated: Se está logado
 * - loading: Se está carregando
 * - error: Mensagem de erro (se houver)
 *
 * Funções:
 * - login(email, password)
 * - register(email, password, first_name, last_name)
 * - logout()
 * - updateUser(data)
 * - refreshToken()
 */

export const AuthContext = React.createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verifica se está autenticado ao montar
    const checkAuth = () => {
      const token = localStorage.getItem('access_token')
      const userData = localStorage.getItem('user')

      if (token && userData) {
        setUser(JSON.parse(userData))
        setIsAuthenticated(true)
      }
      setLoading(false)
    }

    checkAuth()
  }, [])

  const login = async (email, password) => {
    try {
      setLoading(true)
      const response = await api.post('/auth/login/', { email, password })

      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      localStorage.setItem('user', JSON.stringify(response.data.user))

      setUser(response.data.user)
      setIsAuthenticated(true)

      return response.data
    } catch (error) {
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')

    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated, loading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// Hook para usar o context
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider')
  }
  return context
}
```

**Uso em componentes:**

```jsx
function Dashboard() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" />
  }

  return <h1>Bem-vindo, {user.first_name}!</h1>
}
```

### TransactionContext.jsx

```jsx
/**
 * Gerencia estado de transações.
 *
 * Estado:
 * - transactions: Lista de transações
 * - loading: Se está carregando
 * - filters: Filtros aplicados
 * - pagination: Info de paginação
 *
 * Funções:
 * - fetchTransactions(filters)
 * - getTransaction(id)
 * - createTransaction(data)
 * - updateTransaction(id, data)
 * - deleteTransaction(id)
 */

export const TransactionContext = React.createContext()

export function TransactionProvider({ children }) {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    category: null,
    type: null,
    month: new Date().getMonth() + 1
  })
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 20,
    total: 0
  })

  const fetchTransactions = async (newFilters = null) => {
    try {
      setLoading(true)

      const filtersToUse = newFilters || filters
      const params = new URLSearchParams()

      if (filtersToUse.category)
        params.append('category', filtersToUse.category)
      if (filtersToUse.type) params.append('type', filtersToUse.type)

      const response = await api.get(`/transactions/?${params}`)

      setTransactions(response.data.results || response.data)
      setPagination({
        ...pagination,
        total: response.data.count || response.data.length
      })
    } catch (error) {
      console.error('Erro ao buscar transações:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const createTransaction = async data => {
    try {
      const response = await api.post('/transactions/', data)
      setTransactions([response.data, ...transactions])
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateTransaction = async (id, data) => {
    try {
      const response = await api.put(`/transactions/${id}/`, data)
      const updated = transactions.map(t => (t.id === id ? response.data : t))
      setTransactions(updated)
      return response.data
    } catch (error) {
      throw error
    }
  }

  const deleteTransaction = async id => {
    try {
      await api.delete(`/transactions/${id}/`)
      setTransactions(transactions.filter(t => t.id !== id))
    } catch (error) {
      throw error
    }
  }

  return (
    <TransactionContext.Provider
      value={{
        transactions,
        loading,
        filters,
        pagination,
        fetchTransactions,
        createTransaction,
        updateTransaction,
        deleteTransaction
      }}
    >
      {children}
    </TransactionContext.Provider>
  )
}

export const useTransactions = () => {
  const context = useContext(TransactionContext)
  if (!context) {
    throw new Error(
      'useTransactions deve ser usado dentro de TransactionProvider'
    )
  }
  return context
}
```

---

## 🔌 Services (APIs)

### api.js

```jsx
/**
 * Cliente Axios configurado e centralizado.
 *
 * Features:
 * - BaseURL pré-configurada
 * - Headers com token automático
 * - Interceptadores para renovação de token
 * - Tratamento de erros
 */

import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptador de Requisição
api.interceptors.request.use(
  config => {
    // Adiciona token ao header
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Interceptador de Resposta
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // Se receber 401 e não for uma retry
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Tenta renovar o token
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken
        })

        const { access } = response.data
        localStorage.setItem('access_token', access)

        // Retry da requisição original
        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // Se falhar, faz logout
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
```

### auth.js

```jsx
/**
 * Funções relacionadas a autenticação.
 */

import api from './api'

export const authService = {
  /**
   * Registra novo usuário.
   * @param {Object} data - email, password, password_confirm, first_name, last_name
   * @returns {Promise} Dados do usuário criado
   */
  register: data => api.post('/auth/register/', data),

  /**
   * Faz login.
   * @param {string} email
   * @param {string} password
   * @returns {Promise} tokens e dados do usuário
   */
  login: (email, password) => api.post('/auth/login/', { email, password }),

  /**
   * Faz logout (remove tokens localmente).
   */
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },

  /**
   * Solicita reset de senha.
   * @param {string} email
   * @returns {Promise}
   */
  requestPasswordReset: email => api.post('/auth/password-reset/', { email }),

  /**
   * Confirma novo password.
   * @param {Object} data - uid, token, new_password, new_password_confirm
   * @returns {Promise}
   */
  confirmPasswordReset: data => api.post('/auth/password-reset/confirm/', data),

  /**
   * Atualiza perfil do usuário.
   * @param {Object} data - Dados a atualizar
   * @returns {Promise}
   */
  updateProfile: data => api.put('/auth/profile/', data)
}

export default authService
```

### transactions.js

```jsx
/**
 * Funções relacionadas a transações.
 */

import api from './api'

export const transactionService = {
  /**
   * Lista transações com filtros e paginação.
   * @param {Object} filters - { category, type, ordering, page, limit }
   * @returns {Promise} Lista paginada de transações
   */
  list: (filters = {}) => {
    const params = new URLSearchParams(filters)
    return api.get(`/transactions/?${params}`)
  },

  /**
   * Obtém uma transação específica.
   * @param {number} id
   * @returns {Promise}
   */
  get: id => api.get(`/transactions/${id}/`),

  /**
   * Cria nova transação.
   * @param {Object} data - description, amount, category, type
   * @returns {Promise}
   */
  create: data => api.post('/transactions/', data),

  /**
   * Atualiza transação.
   * @param {number} id
   * @param {Object} data - Dados a atualizar
   * @returns {Promise}
   */
  update: (id, data) => api.put(`/transactions/${id}/`, data),

  /**
   * Deleta transação.
   * @param {number} id
   * @returns {Promise}
   */
  delete: id => api.delete(`/transactions/${id}/`),

  /**
   * Gera relatório com resumo mensal.
   * @param {number} month - Mês (1-12)
   * @param {number} year - Ano
   * @returns {Promise}
   */
  getReport: (month, year) =>
    api.get(`/transactions/report/?month=${month}&year=${year}`)
}

export default transactionService
```

### storage.js

```jsx
/**
 * Gerencia dados no localStorage.
 */

export const storageService = {
  // Tokens
  setAccessToken: token => localStorage.setItem('access_token', token),
  getAccessToken: () => localStorage.getItem('access_token'),
  setRefreshToken: token => localStorage.setItem('refresh_token', token),
  getRefreshToken: () => localStorage.getItem('refresh_token'),
  removeTokens: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  // Usuário
  setUser: user => localStorage.setItem('user', JSON.stringify(user)),
  getUser: () => {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },
  removeUser: () => localStorage.removeItem('user'),

  // Preferências
  setTheme: theme => localStorage.setItem('theme', theme),
  getTheme: () => localStorage.getItem('theme') || 'light',

  setLanguage: lang => localStorage.setItem('language', lang),
  getLanguage: () => localStorage.getItem('language') || 'pt-BR'
}

export default storageService
```

---

## 📄 Páginas

### Login.jsx

```jsx
// Página de login
// - Formulário com email e senha
// - Validação client-side
// - Link para "Esqueceu senha?"
// - Link para "Registrar"
// - Redireciona para Dashboard após sucesso
```

### Register.jsx

```jsx
// Página de registro
// - Formulário com email, name, senha, confirmação
// - Validação de senha forte em tempo real
// - Link para "Já tem conta? Faça login"
```

### Dashboard.jsx

```jsx
// Dashboard principal
// - Resumo mensal (receita/despesa)
// - Gráfico de despesas por categoria
// - Últimas transações
// - Cards com estatísticas
```

### Transactions.jsx

```jsx
// Gestão completa de transações
// - Filtros (categoria, tipo, mês)
// - Botão para criar transação
// - Lista com paginação
// - Opções de editar/deletar
```

---

## 🔄 Fluxos de Dados

### Fluxo de Login

```
Usuário preenche form
         ↓
Clica "Entrar"
         ↓
authService.login(email, password)
         ↓
POST /api/auth/login/
         ↓
Backend valida
         ↓
Retorna { access, refresh, user }
         ↓
LocalStorage.setItem('access_token', access)
LocalStorage.setItem('refresh_token', refresh)
LocalStorage.setItem('user', user)
         ↓
AuthContext.login() executa
         ↓
state.user = user
state.isAuthenticated = true
         ↓
Componentes re-renderizam
         ↓
useAuth().isAuthenticated é true
         ↓
Redireciona para /dashboard
```

### Fluxo de Criar Transação

```
Usuário preenche formulário
         ↓
Clica "Salvar"
         ↓
Validação client-side
         ↓
transactionService.create(data)
         ↓
POST /api/transactions/
(Header: Authorization: Bearer token)
         ↓
Backend valida e cria
         ↓
Retorna { id, description, amount, ... }
         ↓
TransactionContext.createTransaction()
         ↓
state.transactions = [nova, ...resto]
         ↓
TransactionList re-renderiza
         ↓
Toast de sucesso
```

### Fluxo de Token Expirado

```
Usuário faz requisição
         ↓
Axios envia com access_token
         ↓
Backend retorna 401 (token expirado)
         ↓
Interceptador detecta 401
         ↓
POST /api/auth/token/refresh/
(Body: { refresh: refresh_token })
         ↓
Backend valida refresh_token
         ↓
Retorna novo { access }
         ↓
localStorage.setItem('access_token', novo_access)
         ↓
Retry requisição original com novo token
         ↓
Requisição sucede
         ↓
Usuário não percebeu nada!
```

---

## 🚀 Deployment

### Vercel

1. Conectar repositório GitHub
2. Framework preset: `Vite`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment variables:
   ```
   VITE_API_URL=https://seu-backend.com/api
   ```

### Build Local

```bash
npm run build
# Gera pasta 'dist' com aplicação pronta para produção
```

### Variáveis de Ambiente

Arquivo `.env` ou `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Financial Dashboard
```

---

## 📚 Referências

- [React Documentation](https://react.dev)
- [React Router](https://reactrouter.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Axios Documentation](https://axios-http.com)
- [Vite Documentation](https://vitejs.dev)

---

**Desenvolvido com ❤️**
