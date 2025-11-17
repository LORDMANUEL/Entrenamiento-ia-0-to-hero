// src/components/Forecast/ForecastResult.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

type HistoryMonth = {
  month: string;
  quantity: number;
};

interface ForecastResultProps {
  prediction: number | null;
  history: HistoryMonth[];
}

const getDemandLevel = (quantity: number | null): { level: string; color: string } => {
    if (quantity === null) return { level: 'N/A', color: 'bg-gray-400' };
    if (quantity < 100) return { level: 'Bajo', color: 'bg-green-500' };
    if (quantity < 200) return { level: 'Medio', color: 'bg-yellow-500' };
    return { level: 'Alto', color: 'bg-red-500' };
};

const ForecastResult: React.FC<ForecastResultProps> = ({ prediction, history }) => {
  if (prediction === null) {
    return (
      <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 flex items-center justify-center h-full">
        <p className="text-gray-500">Esperando parámetros para calcular la predicción...</p>
      </div>
    );
  }

  const { level, color } = getDemandLevel(prediction);

  // Prepare data for the chart
  const chartData = [...history]
    .map(h => ({ name: h.month, Historial: h.quantity }))
    .sort((a, b) => a.name.localeCompare(b.name));

  const lastMonth = history.length > 0 ? history.reduce((max, h) => h.month > max ? h.month : max, history[0].month) : '2024-12';
  const [year, month] = lastMonth.split('-').map(Number);
  const nextMonthDate = new Date(year, month, 1);
  const nextMonthStr = `${nextMonthDate.getFullYear()}-${String(nextMonthDate.getMonth() + 1).padStart(2, '0')}`;

  chartData.push({ name: nextMonthStr, Forecast: prediction, Historial: null });

  return (
    <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 h-full">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Resultado del Forecast</h3>
      <div className="flex items-center justify-between mb-6 p-4 bg-gray-50 rounded-lg">
        <div>
          <p className="text-sm text-gray-600">Demanda estimada próximo mes:</p>
          <p className="text-4xl font-bold text-blue-600">{prediction.toFixed(2)}</p>
          <p className="text-sm text-gray-600">unidades</p>
        </div>
        <div className="text-right">
            <p className="text-sm text-gray-600 mb-1">Nivel de Demanda</p>
            <span className={`px-3 py-1 text-sm font-semibold text-white rounded-full ${color}`}>
                {level}
            </span>
        </div>
      </div>

      <div className="h-72">
        <h4 className="text-lg font-medium text-gray-700 mb-3 text-center">Evolución de la Demanda</h4>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="Historial" stroke="#8884d8" activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="Forecast" stroke="#82ca9d" strokeDasharray="5 5" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ForecastResult;
