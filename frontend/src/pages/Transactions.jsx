import { useState, useEffect } from 'react'
import { useTransactions } from '../contexts/TransactionContext'
import TransactionFilters from '../components/transactions/TransactionFilters'
import TransactionForm from '../components/transactions/TransactionForm'
import Modal from '../components/common/Modal'
import Button from '../components/common/Button'
import toast from 'react-hot-toast'

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

export default function Transactions() {
  const {
    transactions,
    loading,
    filters,
    setFilters,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
  } = useTransactions()
  
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTransaction, setEditingTransaction] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10
  
  useEffect(() => {
    fetchTransactions()
  }, [])
  
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
    setCurrentPage(1)
  }
  
  const handleApplyFilters = () => {
    fetchTransactions(filters)
    setCurrentPage(1)
  }
  
  const handleClearFilters = () => {
    const clearedFilters = { month: '', category: '', type: '' }
    setFilters(clearedFilters)
    fetchTransactions(clearedFilters)
    setCurrentPage(1)
  }
  
  const handleAddTransaction = () => {
    setEditingTransaction(null)
    setIsModalOpen(true)
  }
  
  const handleEditTransaction = (transaction) => {
    setEditingTransaction(transaction)
    setIsModalOpen(true)
  }
  
  const handleDeleteTransaction = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta transação?')) {
      const result = await deleteTransaction(id)
      if (result.success) {
        toast.success('Transação excluída com sucesso!')
      } else {
        toast.error(result.error || 'Erro ao excluir transação')
      }
    }
  }
  
  const handleFormSubmit = async (data) => {
    let result
    if (editingTransaction) {
      result = await updateTransaction(editingTransaction.id, data)
    } else {
      result = await createTransaction(data)
    }
    
    if (result.success) {
      toast.success(
        editingTransaction
          ? 'Transação atualizada com sucesso!'
          : 'Transação criada com sucesso!'
      )
      setIsModalOpen(false)
      setEditingTransaction(null)
    } else {
      toast.error(result.error || 'Erro ao salvar transação')
    }
  }
  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value)
  }
  
  const formatDate = (dateString) => {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(dateString))
  }
  
  useEffect(() => {
    handleApplyFilters()
  }, [filters])
  
  const totalPages = Math.ceil(transactions.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentTransactions = transactions.slice(startIndex, endIndex)
  
  const handlePreviousPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1))
  }
  
  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages))
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Transações</h1>
        <Button onClick={handleAddTransaction}>
          Nova Transação
        </Button>
      </div>
      
      <TransactionFilters
        filters={filters}
        onFilterChange={handleFilterChange}
        onClearFilters={handleClearFilters}
      />
      
      {loading ? (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="animate-pulse">
            <div className="h-12 bg-gray-200"></div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="border-t border-gray-200">
                <div className="h-16 bg-gray-100"></div>
              </div>
            ))}
          </div>
        </div>
      ) : transactions.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhuma transação encontrada</h3>
          <p className="mt-1 text-sm text-gray-500">
            Comece criando uma nova transação.
          </p>
          <div className="mt-6">
            <Button onClick={handleAddTransaction}>
              Nova Transação
            </Button>
          </div>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Categoria
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Descrição
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Valor
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {currentTransactions.map((transaction) => (
                  <tr key={transaction.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(transaction.date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          transaction.transaction_type === 'receita'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {TYPES[transaction.transaction_type]}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {CATEGORIES[transaction.category]}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {transaction.description}
                    </td>
                    <td
                      className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                        transaction.transaction_type === 'receita'
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {formatCurrency(transaction.amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleEditTransaction(transaction)}
                        className="text-blue-600 hover:text-blue-900 mr-4"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDeleteTransaction(transaction.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-6 px-4">
              <div className="text-sm text-gray-700">
                Mostrando {startIndex + 1} a {Math.min(endIndex, transactions.length)} de{' '}
                {transactions.length} transações
              </div>
              <div className="flex gap-2">
                <Button
                  onClick={handlePreviousPage}
                  disabled={currentPage === 1}
                  variant="secondary"
                >
                  Anterior
                </Button>
                <span className="px-4 py-2 text-sm text-gray-700">
                  Página {currentPage} de {totalPages}
                </span>
                <Button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  variant="secondary"
                >
                  Próxima
                </Button>
              </div>
            </div>
          )}
        </>
      )}
      
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setEditingTransaction(null)
        }}
        title={editingTransaction ? 'Editar Transação' : 'Nova Transação'}
      >
        <TransactionForm
          transaction={editingTransaction}
          onSubmit={handleFormSubmit}
          onCancel={() => {
            setIsModalOpen(false)
            setEditingTransaction(null)
          }}
          loading={loading}
        />
      </Modal>
    </div>
  )
}
