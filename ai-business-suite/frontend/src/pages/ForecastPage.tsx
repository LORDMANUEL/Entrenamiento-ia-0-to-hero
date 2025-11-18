// src/pages/ForecastPage.tsx
import { useState } from 'react';
import ForecastForm from '../components/Forecast/ForecastForm';
import ForecastResult from '../components/Forecast/ForecastResult';
import { fetchForecastPrediction } from '../lib/api';
import { PlusCircle, MinusCircle } from 'lucide-react';

type HistoryMonth = {
  month: string;
  quantity: number;
};

// Generate placeholder history for the last 12 months
const generateInitialHistory = (): HistoryMonth[] => {
  const history: HistoryMonth[] = [];
  const today = new Date();
  for (let i = 11; i >= 0; i--) {
    const d = new Date(today.getFullYear(), today.getMonth() - i, 1);
    history.push({
      month: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`,
      quantity: 0,
    });
  }
  return history;
};


const ForecastPage = () => {
  const [itemCode, setItemCode] = useState('ITM001');
  const [whsCode, setWhsCode] = useState('WHS01');
  const [history, setHistory] = useState<HistoryMonth[]>(generateInitialHistory());

  const [prediction, setPrediction] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setPrediction(null);

    // Filter out entries with invalid month format or 0 quantity
    const validHistory = history.filter(h => h.month.match(/^\d{4}-\d{2}$/) && h.quantity > 0);

    if (validHistory.length < 3) {
        setError('Por favor, introduzca al menos 3 meses de historial con cantidad mayor a 0.');
        setIsLoading(false);
        return;
    }

    try {
      const result = await fetchForecastPrediction(itemCode, whsCode, validHistory);
      setPrediction(result.predicted_quantity);
    } catch (err: any) {
      setError(err.message || 'Ocurrió un error al contactar la API.');
    } finally {
      setIsLoading(false);
    }
  };

  const addHistoryRow = () => {
    setHistory(prev => [...prev, { month: '', quantity: 0 }]);
  };

  const removeHistoryRow = (index: number) => {
    setHistory(prev => prev.filter((_, i) => i !== index));
  };


  return (
    <div className="p-8 bg-gray-50/50 min-h-full">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <ForecastForm
            itemCode={itemCode}
            setItemCode={setItemCode}
            whsCode={whsCode}
            setWhsCode={setWhsCode}
            history={history}
            setHistory={setHistory}
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
           {error && (
            <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg shadow-md">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>
        <div>
          <ForecastResult prediction={prediction} history={history.filter(h => h.quantity > 0)} />
        </div>
      </div>
    </div>
  );
};

export default ForecastPage;
