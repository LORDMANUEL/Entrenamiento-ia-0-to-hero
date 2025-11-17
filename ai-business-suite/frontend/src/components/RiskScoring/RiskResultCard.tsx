// src/components/RiskScoring/RiskResultCard.tsx
import { RiskScoringResponse } from '../../lib/api';

interface RiskResultCardProps {
  result: RiskScoringResponse | null;
}

const getBucketStyle = (bucket: 'BAJO' | 'MEDIO' | 'ALTO' | null) => {
  switch (bucket) {
    case 'BAJO':
      return { text: 'text-green-600', bg: 'bg-green-100', border: 'border-green-500' };
    case 'MEDIO':
      return { text: 'text-yellow-600', bg: 'bg-yellow-100', border: 'border-yellow-500' };
    case 'ALTO':
      return { text: 'text-red-600', bg: 'bg-red-100', border: 'border-red-500' };
    default:
      return { text: 'text-gray-600', bg: 'bg-gray-100', border: 'border-gray-400' };
  }
};

const RiskResultCard: React.FC<RiskResultCardProps> = ({ result }) => {
  if (!result) {
    return (
        <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 flex items-center justify-center h-full">
            <p className="text-gray-500">El resultado del análisis de riesgo aparecerá aquí.</p>
        </div>
    );
  }

  const bucketStyle = getBucketStyle(result.bucket);
  const probabilityPercentage = (result.prob_riesgo * 100).toFixed(2);

  return (
    <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 h-full">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Resultado del Análisis</h3>

      <div className={`p-4 rounded-lg border-2 ${bucketStyle.bg} ${bucketStyle.border} text-center mb-6`}>
        <p className="text-sm font-medium">Nivel de Riesgo</p>
        <p className={`text-3xl font-bold ${bucketStyle.text}`}>{result.bucket}</p>
      </div>

      <div className="mb-6">
        <h4 className="text-lg font-medium text-gray-700 mb-2">Probabilidad de Atraso</h4>
        {/* Gauge Chart */}
        <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden relative border">
          <div
            className="bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 h-full"
            style={{ width: `${probabilityPercentage}%` }}
          />
          <div
            className="absolute top-0 h-full w-1 bg-black"
            style={{ left: `calc(${probabilityPercentage}% - 2px)` }}
          ></div>
          <span className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 font-bold text-gray-800 mix-blend-screen">
            {probabilityPercentage}%
          </span>
        </div>
        <div className="flex justify-between text-xs mt-1">
          <span>Bajo</span>
          <span>Medio</span>
          <span>Alto</span>
        </div>
      </div>

      <div>
        <h4 className="text-lg font-medium text-gray-700 mb-2">Explicación del Modelo</h4>
        <p className="p-4 bg-gray-50 rounded-lg text-gray-600 text-sm border">
          {result.explanation}
        </p>
      </div>
    </div>
  );
};

export default RiskResultCard;
