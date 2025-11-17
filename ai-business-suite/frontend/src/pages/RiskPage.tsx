// src/pages/RiskPage.tsx
import { useState } from 'react';
import RiskForm from '../components/RiskScoring/RiskForm';
import RiskResultCard from '../components/RiskScoring/RiskResultCard';
import { fetchRiskScore, RiskScoringRequest, RiskScoringResponse } from '../lib/api';

const RiskPage = () => {
  const [formData, setFormData] = useState<RiskScoringRequest>({
    segment: 'Retail',
    city: 'Madrid',
    amount: 1000,
    payment_terms_days: 30,
    past_due_count: 0,
    avg_days_past_due: 0,
  });

  const [result, setResult] = useState<RiskScoringResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiResponse = await fetchRiskScore(formData);
      setResult(apiResponse);
    } catch (err: any) {
      setError(err.message || 'Ocurrió un error al calcular el riesgo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 bg-gray-50/50 min-h-full">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <RiskForm
            formData={formData}
            setFormData={setFormData}
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
          <RiskResultCard result={result} />
        </div>
      </div>
    </div>
  );
};

export default RiskPage;
