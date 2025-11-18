// src/pages/TicketsPage.tsx
import { useState } from 'react';
import TicketForm from '../components/Tickets/TicketForm';
import TicketResult from '../components/Tickets/TicketResult';
import {
  fetchTicketClassification,
  fetchTicketSuggestions,
  TicketClassificationResponse,
  TicketSuggestionResponse
} from '../lib/api';

type ApiResult = TicketClassificationResponse | TicketSuggestionResponse;

const TicketsPage = () => {
  const [description, setDescription] = useState('');
  const [result, setResult] = useState<ApiResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClassify = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const apiResponse = await fetchTicketClassification(description);
      setResult(apiResponse);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggest = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const apiResponse = await fetchTicketSuggestions(description);
      setResult(apiResponse);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 bg-gray-50/50 min-h-full">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full">
        <div className="lg:h-[calc(100vh-8rem)]">
          <TicketForm
            description={description}
            setDescription={setDescription}
            onClassify={handleClassify}
            onSuggest={handleSuggest}
            isLoading={isLoading}
          />
        </div>
        <div className="lg:h-[calc(100vh-8rem)]">
          <TicketResult result={result} />
        </div>
      </div>
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg shadow-md fixed bottom-8 left-1/2 -translate-x-1/2">
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
};

export default TicketsPage;
