// src/components/RiskScoring/RiskForm.tsx
import React from 'react';
import { RiskScoringRequest } from '../../lib/api';

interface RiskFormProps {
  formData: RiskScoringRequest;
  setFormData: (data: RiskScoringRequest) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

const RiskForm: React.FC<RiskFormProps> = ({ formData, setFormData, onSubmit, isLoading }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: e.target.type === 'number' ? parseFloat(value) || 0 : value,
    });
  };

  return (
    <form onSubmit={onSubmit} className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Datos de la Operación</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="segment" className="block text-sm font-medium text-gray-600 mb-1">Segmento</label>
          <select
            id="segment"
            name="segment"
            value={formData.segment}
            onChange={handleChange}
            className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="Retail">Retail</option>
            <option value="Empresa">Empresa</option>
            <option value="Gobierno">Gobierno</option>
          </select>
        </div>
        <div>
          <label htmlFor="city" className="block text-sm font-medium text-gray-600 mb-1">Ciudad</label>
          <input type="text" id="city" name="city" value={formData.city} onChange={handleChange} required className="w-full px-4 py-2 bg-gray-50 border rounded-lg" />
        </div>
        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-600 mb-1">Monto</label>
          <input type="number" id="amount" name="amount" value={formData.amount} onChange={handleChange} required className="w-full px-4 py-2 bg-gray-50 border rounded-lg" />
        </div>
        <div>
          <label htmlFor="payment_terms_days" className="block text-sm font-medium text-gray-600 mb-1">Plazo (días)</label>
          <input type="number" id="payment_terms_days" name="payment_terms_days" value={formData.payment_terms_days} onChange={handleChange} required className="w-full px-4 py-2 bg-gray-50 border rounded-lg" />
        </div>
        <div>
          <label htmlFor="past_due_count" className="block text-sm font-medium text-gray-600 mb-1">Veces en Mora</label>
          <input type="number" id="past_due_count" name="past_due_count" value={formData.past_due_count} onChange={handleChange} required className="w-full px-4 py-2 bg-gray-50 border rounded-lg" />
        </div>
        <div>
          <label htmlFor="avg_days_past_due" className="block text-sm font-medium text-gray-600 mb-1">Días Promedio en Mora</label>
          <input type="number" id="avg_days_past_due" name="avg_days_past_due" value={formData.avg_days_past_due} onChange={handleChange} required className="w-full px-4 py-2 bg-gray-50 border rounded-lg" />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="mt-8 w-full py-3 px-6 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-transform transform hover:scale-105 disabled:bg-gray-400"
      >
        {isLoading ? 'Calculando...' : 'Calcular Riesgo'}
      </button>
    </form>
  );
};

export default RiskForm;
