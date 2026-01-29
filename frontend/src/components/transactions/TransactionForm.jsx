import { useState, useEffect } from 'react'
import Button from '../common/Button'

const CATEGORIES = {
  alimentacao: 'Alimentação',
  transporte: 'Transporte',
  moradia: 'Moradia',
  saude: 'Saúde',
  lazer: 'Lazer',
  educacao: 'Educação',
  salario: 'Salário',
  investimentos: 'Investimentos',
  outros: 'Outros',
}

const TYPES = {
  receita: 'Receita',
  despesa: 'Despesa',
}

export default function TransactionForm({ transaction, onSubmit, onCancel, loading }) {
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    category: '',
    transaction_type: '',
    date: '',
  })
  
  const [errors, setErrors] = useState({})
  
  useEffect(() => {
    if (transaction) {
      setFormData({
        amount: transaction.amount || '',
        description: transaction.description || '',
        category: transaction.category || '',
        transaction_type: transaction.transaction_type || '',
        date: transaction.date || '',
      })
    } else {
      const today = new Date().toISOString().split('T')[0]
      setFormData({
        amount: '',
        description: '',
        category: '',
        transaction_type: '',
        date: today,
      })
    }
  }, [transaction])
  
  const validate = () => {
    const newErrors = {}
    
    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'O valor deve ser maior que zero'
    }
    
    if (!formData.description || formData.description.trim().length === 0) {
      newErrors.description = 'A descrição é obrigatória'
    }
    
    if (!formData.category) {
      newErrors.category = 'A categoria é obrigatória'
    }
    
    if (!formData.transaction_type) {
      newErrors.transaction_type = 'O tipo é obrigatório'
    }
    
    if (!formData.date) {
      newErrors.date = 'A data é obrigatória'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }
  
  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (validate()) {
      onSubmit(formData)
    }
  }
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }))
    }
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
          Valor *
        </label>
        <input
          type="number"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          step="0.01"
          min="0"
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.amount ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        {errors.amount && (
          <p className="mt-1 text-sm text-red-600">{errors.amount}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Descrição *
        </label>
        <input
          type="text"
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.description ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
          Categoria *
        </label>
        <select
          id="category"
          name="category"
          value={formData.category}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.category ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="">Selecione uma categoria</option>
          {Object.entries(CATEGORIES).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        {errors.category && (
          <p className="mt-1 text-sm text-red-600">{errors.category}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="transaction_type" className="block text-sm font-medium text-gray-700 mb-1">
          Tipo *
        </label>
        <select
          id="transaction_type"
          name="transaction_type"
          value={formData.transaction_type}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.transaction_type ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="">Selecione um tipo</option>
          {Object.entries(TYPES).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        {errors.transaction_type && (
          <p className="mt-1 text-sm text-red-600">{errors.transaction_type}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
          Data *
        </label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.date ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        {errors.date && (
          <p className="mt-1 text-sm text-red-600">{errors.date}</p>
        )}
      </div>
      
      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          variant="primary"
          loading={loading}
          fullWidth
        >
          {transaction ? 'Atualizar' : 'Criar'}
        </Button>
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={loading}
          fullWidth
        >
          Cancelar
        </Button>
      </div>
    </form>
  )
}
