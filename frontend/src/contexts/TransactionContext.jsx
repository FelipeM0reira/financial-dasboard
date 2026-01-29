import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const TransactionContext = createContext(null)

// Normalize transaction data from backend to frontend format
function normalizeTransaction(transaction) {
  return {
    ...transaction,
    type: transaction.transaction_type === 'receita' ? 'income' : 'expense',
    type_display: transaction.type_display || (transaction.transaction_type === 'receita' ? 'Receita' : 'Despesa'),
    category_display: transaction.category_display || transaction.category,
  }
}

export function TransactionProvider({ children }) {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({
    month: '',
    category: '',
    type: '',
  })
  const [report, setReport] = useState(null)

  // Load transactions when component mounts if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchTransactions()
    }
  }, [])

  const fetchTransactions = async (filterParams) => {
    setLoading(true)
    setError(null)
    try {
      const params = filterParams || filters
      const queryParams = new URLSearchParams()
      
      if (params.month) queryParams.append('month', params.month)
      if (params.category) queryParams.append('category', params.category)
      if (params.type) queryParams.append('type', params.type)
      
      const response = await api.get(`/transactions/?${queryParams.toString()}`)
      const transactions = response.data.results || response.data
      const normalized = Array.isArray(transactions) 
        ? transactions.map(normalizeTransaction)
        : transactions
      setTransactions(normalized)
      return { success: true, data: response.data }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          'Failed to fetch transactions.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const createTransaction = async (data) => {
    setLoading(true)
    setError(null)
    try {
      // Convert frontend format to backend format
      const backendData = {
        ...data,
        transaction_type: data.type === 'income' ? 'receita' : 'despesa'
      }
      delete backendData.type
      
      const response = await api.post('/transactions/', backendData)
      const normalized = normalizeTransaction(response.data)
      setTransactions((prev) => [normalized, ...prev])
      return { success: true, data: normalized }
    } catch (err) {
      const errorMessage = err.response?.data?.amount?.[0] || 
                          err.response?.data?.category?.[0] || 
                          err.response?.data?.detail || 
                          'Failed to create transaction.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const updateTransaction = async (id, data) => {
    setLoading(true)
    setError(null)
    try {
      // Convert frontend format to backend format
      const backendData = {
        ...data,
        transaction_type: data.type === 'income' ? 'receita' : 'despesa'
      }
      delete backendData.type
      
      const response = await api.put(`/transactions/${id}/`, backendData)
      const normalized = normalizeTransaction(response.data)
      setTransactions((prev) =>
        prev.map((transaction) =>
          transaction.id === id ? normalized : transaction
        )
      )
      return { success: true, data: normalized }
    } catch (err) {
      const errorMessage = err.response?.data?.amount?.[0] || 
                          err.response?.data?.category?.[0] || 
                          err.response?.data?.detail || 
                          'Failed to update transaction.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const deleteTransaction = async (id) => {
    setLoading(true)
    setError(null)
    try {
      await api.delete(`/transactions/${id}/`)
      setTransactions((prev) =>
        prev.filter((transaction) => transaction.id !== id)
      )
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          'Failed to delete transaction.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const fetchReport = async (month) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/transactions/report/?month=${month}`)
      setReport(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          'Failed to fetch report.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const exportCSV = async (month) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/transactions/export/?month=${month}`, {
        responseType: 'blob',
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `transactions_${month}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          'Failed to export CSV.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const value = {
    transactions,
    loading,
    error,
    filters,
    report,
    setFilters,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    fetchReport,
    exportCSV,
  }

  return (
    <TransactionContext.Provider value={value}>
      {children}
    </TransactionContext.Provider>
  )
}

export function useTransactions() {
  const context = useContext(TransactionContext)
  if (!context) {
    throw new Error('useTransactions must be used within a TransactionProvider')
  }
  return context
}
