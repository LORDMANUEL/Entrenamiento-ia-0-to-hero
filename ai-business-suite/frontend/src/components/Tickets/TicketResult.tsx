// src/components/Tickets/TicketResult.tsx
import { TicketClassificationResponse, TicketSuggestionResponse } from '../../lib/api';
import { Lightbulb, CheckCircle } from 'lucide-react';

interface TicketResultProps {
  result: TicketClassificationResponse | TicketSuggestionResponse | null;
}

const TicketResult: React.FC<TicketResultProps> = ({ result }) => {
  if (!result) {
    return (
      <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 flex items-center justify-center h-full">
        <p className="text-gray-500">Los resultados del análisis aparecerán aquí.</p>
      </div>
    );
  }

  const confidencePercentage = 'score_confianza' in result ? (result.score_confianza * 100).toFixed(1) : null;

  return (
    <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 h-full">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Análisis por IA</h3>

      <div className="p-4 bg-gray-50 rounded-lg border mb-6">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-sm text-gray-600">Categoría Predicha</p>
            <p className="text-2xl font-bold text-blue-600">{result.categoria_predicha}</p>
          </div>
          {confidencePercentage && (
             <div className="text-right">
                <p className="text-sm text-gray-600">Confianza</p>
                <p className="text-xl font-semibold text-green-600">{confidencePercentage}%</p>
             </div>
          )}
        </div>
      </div>

      {'soluciones_sugeridas' in result && result.soluciones_sugeridas.length > 0 && (
        <div>
          <h4 className="text-lg font-medium text-gray-700 mb-3 flex items-center">
            <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
            Soluciones Sugeridas
          </h4>
          <ul className="space-y-3">
            {result.soluciones_sugeridas.map((sol, index) => (
              <li key={index} className="p-3 bg-gray-50 rounded-lg border hover:border-blue-400 transition">
                <p className="font-semibold text-gray-800">{sol.resumen}</p>
                <p className="text-xs text-gray-500 mt-1">
                  Basado en Ticket: <span className="font-mono">{sol.fuente_ticket_id}</span> |
                  Similitud: <span className="font-medium">{(sol.similarity_score * 100).toFixed(1)}%</span>
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}

       {'soluciones_sugeridas' in result && result.soluciones_sugeridas.length === 0 && (
            <div className="text-center p-4">
                <p className="text-gray-500">No se encontraron soluciones similares en el historial.</p>
            </div>
       )}

    </div>
  );
};

export default TicketResult;
