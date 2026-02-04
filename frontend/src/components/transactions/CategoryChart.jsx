import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

// Color palette for categories (Portuguese names)
const CATEGORY_COLORS = {
  alimentacao: '#FF6B6B', // Red
  transporte: '#4ECDC4', // Turquoise
  moradia: '#45B7D1', // Blue
  saude: '#96CEB4', // Green
  lazer: '#FFEAA7', // Yellow
  educacao: '#DDA15E', // Brown
  salario: '#06A77D', // Dark Green
  investimentos: '#9B59B6', // Purple
  outros: '#95A5A6' // Gray
}

// Display names for categories
const CATEGORY_NAMES = {
  alimentacao: 'Alimentação',
  transporte: 'Transporte',
  moradia: 'Moradia',
  saude: 'Saúde',
  lazer: 'Lazer',
  educacao: 'Educação',
  salario: 'Salário',
  investimentos: 'Investimentos',
  outros: 'Outros'
}

export default function CategoryChart({ transactions }) {
  // Filter only expenses
  const expenses = transactions.filter(t => t.type === 'expense')

  // Group by category
  const categoryTotals = expenses.reduce((acc, transaction) => {
    const category = transaction.category || 'outros'
    acc[category] = (acc[category] || 0) + parseFloat(transaction.amount)
    return acc
  }, {})

  const categories = Object.keys(categoryTotals)
  const totals = Object.values(categoryTotals)

  const backgroundColors = categories.map(
    cat => CATEGORY_COLORS[cat] || '#95A5A6'
  )
  const borderColors = backgroundColors.map(color => color)

  const data = {
    labels: categories.map(cat => CATEGORY_NAMES[cat] || cat),
    datasets: [
      {
        label: 'Despesas por Categoria',
        data: totals,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 15,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const label = context.label || ''
            const value = new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
            }).format(context.parsed)
            return `${label}: ${value}`
          }
        }
      }
    }
  }

  if (expenses.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Despesas por Categoria
        </h2>
        <div className="flex items-center justify-center h-64 text-gray-400">
          <div className="text-center">
            <svg
              className="w-16 h-16 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            <p className="text-sm">Nenhuma despesa registrada</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Despesas por Categoria
      </h2>
      <div className="h-64">
        <Doughnut data={data} options={options} />
      </div>
    </div>
  )
}
