import { useMemo } from 'react'

export default function MonthlyTrend({ transactions }) {
  // Calculate monthly trends for the last 6 months
  const monthlyData = useMemo(() => {
    if (!transactions || transactions.length === 0) {
      return []
    }

    // Get last 6 months
    const months = []
    const today = new Date()

    for (let i = 5; i >= 0; i--) {
      const date = new Date(today.getFullYear(), today.getMonth() - i, 1)
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
      months.push({
        monthKey,
        label: date.toLocaleDateString('pt-BR', {
          month: 'short',
          year: '2-digit'
        }),
        income: 0,
        expense: 0
      })
    }

    // Aggregate transactions by month
    transactions.forEach(transaction => {
      const date = new Date(transaction.date)
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`

      const monthData = months.find(m => m.monthKey === monthKey)
      if (monthData) {
        const amount = parseFloat(transaction.amount)
        if (transaction.type === 'income') {
          monthData.income += amount
        } else {
          monthData.expense += amount
        }
      }
    })

    return months
  }, [transactions])

  if (
    monthlyData.length === 0 ||
    monthlyData.every(m => m.income === 0 && m.expense === 0)
  ) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6 flex items-center justify-center h-80">
        <div className="text-center text-gray-400">
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
              d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
            />
          </svg>
          <p className="text-sm">No data available for the selected period</p>
        </div>
      </div>
    )
  }

  const maxValue = Math.max(
    ...monthlyData.map(m => Math.max(m.income, m.expense))
  )
  const chartHeight = 200
  const chartWidth = monthlyData.length * 50

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Monthly Trend
      </h2>

      <div className="overflow-x-auto">
        <div className="flex items-end justify-around h-80 gap-2 p-4 bg-gray-50 rounded-lg">
          {monthlyData.map((month, index) => {
            const incomeHeight = (month.income / maxValue) * chartHeight
            const expenseHeight = (month.expense / maxValue) * chartHeight

            return (
              <div
                key={index}
                className="flex flex-col items-center gap-2 flex-1"
              >
                {/* Income Bar */}
                <div className="relative h-full w-full flex items-end justify-center gap-1">
                  <div
                    className="w-4 bg-green-500 rounded-t-lg hover:bg-green-600 transition"
                    style={{ height: `${incomeHeight}px`, minHeight: '2px' }}
                    title={`Income: R$ ${month.income.toFixed(2)}`}
                  />
                  {/* Expense Bar */}
                  <div
                    className="w-4 bg-red-500 rounded-t-lg hover:bg-red-600 transition"
                    style={{ height: `${expenseHeight}px`, minHeight: '2px' }}
                    title={`Expense: R$ ${month.expense.toFixed(2)}`}
                  />
                </div>

                {/* Month Label */}
                <div className="text-xs font-medium text-gray-600 text-center whitespace-nowrap">
                  {month.label}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="flex gap-6 mt-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full" />
          <span className="text-sm text-gray-600">Income</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-500 rounded-full" />
          <span className="text-sm text-gray-600">Expense</span>
        </div>
      </div>
    </div>
  )
}
