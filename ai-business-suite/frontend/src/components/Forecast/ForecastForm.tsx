// src/components/Forecast/ForecastForm.tsx
import React from 'react';

type HistoryMonth = {
  month: string;
  quantity: number;
};

interface ForecastFormProps {
  itemCode: string;
  setItemCode: (value: string) => void;
  whsCode: string;
  setWhsCode: (value: string) => void;
  history: HistoryMonth[];
  setHistory: (history: HistoryMonth[]) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

const ForecastForm: React.FC<ForecastFormProps> = ({
  itemCode,
  setItemCode,
  whsCode,
  setWhsCode,
  history,
  setHistory,
  onSubmit,
  isLoading,
}) => {
  const handleHistoryChange = (index: number, field: keyof HistoryMonth, value: string) => {
    const newHistory = [...history];
    const item = newHistory[index];

    if (field === 'month') {
        item.month = value;
    } else if (field === 'quantity') {
        // Allow empty input for user experience, default to 0 for calculations
        item.quantity = value === '' ? 0 : parseFloat(value);
    }

    setHistory(newHistory);
  };

  return (
    <form onSubmit={onSubmit} className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Parámetros de Proyección</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label htmlFor="itemCode" className="block text-sm font-medium text-gray-600 mb-1">
            Item Code
          </label>
          <input
            id="itemCode"
            type="text"
            value={itemCode}
            onChange={(e) => setItemCode(e.target.value)}
            className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            placeholder="Ej: ITM001"
            required
          />
        </div>
        <div>
          <label htmlFor="whsCode" className="block text-sm font-medium text-gray-600 mb-1">
            Almacén
          </label>
          <input
            id="whsCode"
            type="text"
            value={whsCode}
            onChange={(e) => setWhsCode(e.target.value)}
            className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            placeholder="Ej: WHS01"
            required
          />
        </div>
      </div>

      <div className="mb-6">
        <h4 className="text-lg font-medium text-gray-700 mb-3">Histórico de Ventas (Últimos 12 meses)</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-100 text-gray-600 uppercase">
              <tr>
                <th className="px-4 py-2 rounded-l-lg">Mes (YYYY-MM)</th>
                <th className="px-4 py-2 rounded-r-lg">Cantidad</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row, index) => (
                <tr key={index} className="border-b border-gray-200">
                  <td className="px-4 py-2">
                    <input
                      type="text"
                      value={row.month}
                      onChange={(e) => handleHistoryChange(index, 'month', e.target.value)}
                      className="w-full bg-transparent focus:outline-none"
                      placeholder="2024-10"
                      required
                      pattern="\d{4}-\d{2}"
                    />
                  </td>
                  <td className="px-4 py-2">
                    <input
                      type="number"
                      value={row.quantity || ''}
                      onChange={(e) => handleHistoryChange(index, 'quantity', e.target.value)}
                      className="w-full bg-transparent focus:outline-none"
                      placeholder="150"
                      required
                      min="0"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-3 px-6 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-transform transform hover:scale-105 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Calculando...' : 'Calcular Forecast'}
      </button>
    </form>
  );
};

export default ForecastForm;
