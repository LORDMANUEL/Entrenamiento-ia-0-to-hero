// src/components/Tickets/TicketForm.tsx
import React from 'react';

interface TicketFormProps {
  description: string;
  setDescription: (value: string) => void;
  onClassify: () => void;
  onSuggest: () => void;
  isLoading: boolean;
}

const TicketForm: React.FC<TicketFormProps> = ({
  description,
  setDescription,
  onClassify,
  onSuggest,
  isLoading,
}) => {
  return (
    <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200 h-full flex flex-col">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Descripción del Ticket</h3>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        className="w-full flex-grow px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition resize-none"
        placeholder="Describa el problema del cliente o la orden de trabajo aquí..."
        rows={15}
        required
      />
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
        <button
          onClick={onClassify}
          disabled={isLoading || description.length < 10}
          className="py-3 px-6 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {isLoading ? 'Clasificando...' : 'Clasificar Ticket'}
        </button>
        <button
          onClick={onSuggest}
          disabled={isLoading || description.length < 10}
          className="py-3 px-6 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 disabled:bg-gray-400"
        >
          {isLoading ? 'Buscando...' : 'Sugerir Solución'}
        </button>
      </div>
    </div>
  );
};

export default TicketForm;
