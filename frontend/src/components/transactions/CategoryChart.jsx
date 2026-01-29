import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

export default function CategoryChart({ transactions }) {
  // Filter only expenses
  const expenses = transactions.filter(t => t.type === 'expense')

  // Group by category
  const categoryTotals = expenses.reduce((acc, transaction) => {
    const category = transaction.category || 'Other'
    acc[category] = (acc[category] || 0) + parseFloat(transaction.amount)
    return acc
  }, {})

  const categories = Object.keys(categoryTotals)
  const totals = Object.values(categoryTotals)

  // Define colors for categories
  const categoryColors = {
    Food: '#10B981',
    Transport: '#3B82F6',
    Entertainment: '#F59E0B',
    Shopping: '#EC4899',
    Healthcare: '#EF4444',
    Bills: '#8B5CF6',
    Education: '#06B6D4',
    Other: '#6B7280',
  }

  const backgroundColors = categories.map(cat => categoryColors[cat] || '#9CA3AF')
  const borderColors = backgroundColors.map(color => color)

  const data = {
    labels: categories,
    datasets: [
      {
        label: 'Expenses by Category',
        data: totals,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2,
      },
    ],
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
            size: 12,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || ''
            const value = new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
            }).format(context.parsed)
            return `${label}: ${value}`
          }
        }
      }
    },
  }

  if (expenses.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Expenses by Category</h2>
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
            <p className="text-sm">No expense data available</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Expenses by Category</h2>
      <div className="h-64">
        <Doughnut data={data} options={options} />
      </div>
    </div>
  )
}
