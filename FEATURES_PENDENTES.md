# Features Pendentes e Melhorias

## 🎯 Prioridade Alta - Próximos Sprints

### 1. **Transações Recorrentes (Fixas)**
**Status:** Planning  
**Descrição:** Permitir que usuários criem transações que se repetem automaticamente (mensal, semanal, etc)

**Subtasks:**
- [ ] Backend: Criar modelo `RecurringTransaction`
  - Campos: user, description, amount, category, transaction_type, frequency, next_execution_date, active
  - Frequency choices: MONTHLY, WEEKLY, DAILY, YEARLY
- [ ] Backend: Criar job automático (celery/beat) para gerar transações recorrentes
- [ ] Backend: API endpoints CRUD para transações recorrentes
- [ ] Frontend: Página/Modal para gerenciar transações recorrentes
- [ ] Frontend: Indicador visual de transações recorrentes na listagem

**Exemplo de Uso:**
- Aluguel fixo todo mês: R$ 1.500
- Assinatura Netflix toda semana: R$ 50
- Freelance mensal: R$ 2.000

---

### 2. **Cores Customizáveis para Gráficos**
**Status:** Planning  
**Descrição:** Permitir cores diferentes para cada categoria/tipo de transação nos gráficos

**Subtasks:**
- [ ] Backend: Estender modelo `Transaction` com campo `color` opcional
- [ ] Frontend: Criar paleta de cores padrão para categorias
  - alimentacao: #FF6B6B (vermelho)
  - transporte: #4ECDC4 (turquesa)
  - moradia: #45B7D1 (azul)
  - saude: #96CEB4 (verde)
  - lazer: #FFEAA7 (amarelo)
  - educacao: #DDA15E (marrom)
  - salario: #06A77D (verde escuro)
  - investimentos: #9B59B6 (roxo)
  - outros: #95A5A6 (cinza)
- [ ] Frontend: Modal para customizar cores por categoria
- [ ] Frontend: Atualizar CategoryChart para usar cores customizadas
- [ ] Frontend: Salvar preferências de cores no localStorage

**Exemplo:**
```javascript
// Chart atualizado com cores por categoria
const chartData = {
  labels: ['Alimentação', 'Transporte', 'Moradia'],
  datasets: [{
    data: [250.50, 35.00, 1500],
    backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1'] // cores por categoria
  }]
}
```

---

## 📋 Prioridade Média - Próximos Passos

### 3. **Testes Automatizados (Frontend)**
**Status:** Planning  
**Descrição:** Adicionar cobertura de testes com Jest + React Testing Library

**Subtasks:**
- [ ] Setup Jest + React Testing Library
- [ ] Testes das páginas:
  - [ ] Login.test.jsx
  - [ ] Register.test.jsx
  - [ ] Dashboard.test.jsx
  - [ ] Transactions.test.jsx
- [ ] Testes dos componentes críticos:
  - [ ] TransactionForm.test.jsx
  - [ ] Button.test.jsx
  - [ ] Modal.test.jsx
- [ ] Cobertura mínima: 60%

---

### 4. **Deploy para Produção**
**Status:** Planning  
**Descrição:** Publicar aplicação em Render (backend) e Vercel (frontend)

**Subtasks:**
- [ ] Backend - Render:
  - [ ] Criar conta Render
  - [ ] Conectar repositório GitHub
  - [ ] Configurar environment variables
  - [ ] Setup PostgreSQL
  - [ ] Testar deploy
- [ ] Frontend - Vercel:
  - [ ] Criar conta Vercel
  - [ ] Conectar repositório GitHub
  - [ ] Configurar VITE_API_URL
  - [ ] Testar deploy
- [ ] Testes end-to-end em produção

---

### 5. **Melhorias de UX/UI**
**Status:** Planning  
**Descrição:** Polir interface e melhorar experiência do usuário

**Subtasks:**
- [ ] Implementar Sidebar/Navigation
- [ ] Adicionar TransactionList component (tabela)
- [ ] Melhorar responsividade mobile
- [ ] Adicionar Dark Mode
- [ ] Melhorar validação de formulários
- [ ] Adicionar tooltips e help text

---

## 🔄 Prioridade Baixa - Nice-to-Have

### 6. **Budget Goals por Categoria**
Permitir que usuários definem orçamentos máximos por categoria e recebam alertas quando ultrapassarem.

### 7. **Multi-Currency Support**
Suportar múltiplas moedas com conversão automática.

### 8. **Data Export Avançada**
Exportar para PDF, Excel, além de CSV.

### 9. **Análise Avançada**
- Tendências mensais
- Comparação período a período
- Previsões baseadas em histórico

### 10. **Two-Factor Authentication**
Segurança adicional com 2FA via email/SMS.

---

## ✅ Histórico de Conclusões

### Sprint 1 (29/01/2026)
- ✅ Corrigir Docker migrations
- ✅ Implementar CurrentUserView endpoint
- ✅ Normalizar dados frontend/backend
- ✅ Permitir criar/editar receitas e despesas

---

## 🗺️ Roadmap Visual

```
Sprint 1 ✅        Sprint 2 (Próximo)        Sprint 3              Sprint 4+
---------          ----------------         --------              ---------
✅ Docker          - Transações Fixas        - Testes Frontend     - Deploy
✅ Backend APIs    - Cores Gráficos          - Deploy Produção     - Budget Goals
✅ Frontend        - Componentes             - Dark Mode           - Análise Avançada
  Integration        Faltantes                - UI Polish            - 2FA
```
