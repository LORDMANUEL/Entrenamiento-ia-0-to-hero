// src/lib/api.ts

// Define the structure of the API responses to ensure type safety
interface ForecastResponse {
  predicted_quantity: number;
  model_version: string;
}

interface ApiError {
  detail: string;
}

/**
 * Fetches the forecast prediction from the API.
 *
 * @param itemCode The code of the item to forecast.
 * @param whsCode The warehouse code.
 * @param historyMonths An array of historical sales data.
 * @returns The prediction data from the API.
 * @throws An error if the API call fails.
 */
export const fetchForecastPrediction = async (
  itemCode: string,
  whsCode: string,
  historyMonths: { month: string; quantity: number }[]
): Promise<ForecastResponse> => {

  const body = JSON.stringify({
    item_code: itemCode,
    whs_code: whsCode,
    // Ensure quantity is a float, as required by the backend schema
    history_months: historyMonths.map(h => ({ ...h, quantity: Number(h.quantity) || 0 })),
  });

  const response = await fetch('http://localhost:8000/api/forecast/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: body,
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.detail || 'An unknown error occurred.');
  }

  return await response.json() as ForecastResponse;
};

// Types for Risk Scoring
export interface RiskScoringRequest {
  segment: string;
  city: string;
  amount: number;
  payment_terms_days: number;
  past_due_count: number;
  avg_days_past_due: number;
}

export interface RiskScoringResponse {
  prob_riesgo: number;
  bucket: 'BAJO' | 'MEDIO' | 'ALTO';
  explanation: string;
  model_version: string;
}

/**
 * Fetches the risk score from the API.
 */
export const fetchRiskScore = async (
  data: RiskScoringRequest
): Promise<RiskScoringResponse> => {
  const response = await fetch('http://localhost:8000/api/risk/score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.detail || 'Failed to calculate risk score.');
  }

  return await response.json() as RiskScoringResponse;
};

// Types for NLP Tickets
export interface TicketClassificationResponse {
  categoria_predicha: string;
  score_confianza: number;
  model_version: string;
}

export interface SuggestedSolution {
  resumen: string;
  fuente_ticket_id: string;
  similarity_score: number;
}

export interface TicketSuggestionResponse {
  categoria_predicha: string;
  soluciones_sugeridas: SuggestedSolution[];
  model_version: string;
}

/**
 * Fetches the ticket classification from the API.
 */
export const fetchTicketClassification = async (
  descripcion: string
): Promise<TicketClassificationResponse> => {
  const response = await fetch('http://localhost:8000/api/tickets/classify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descripcion }),
  });
  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.detail || 'Failed to classify ticket.');
  }
  return await response.json() as TicketClassificationResponse;
};

/**
 * Fetches solution suggestions from the API.
 */
export const fetchTicketSuggestions = async (
  descripcion: string
): Promise<TicketSuggestionResponse> => {
  const response = await fetch('http://localhost:8000/api/tickets/suggest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descripcion }),
  });
  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.detail || 'Failed to get suggestions.');
  }
  return await response.json() as TicketSuggestionResponse;
};
