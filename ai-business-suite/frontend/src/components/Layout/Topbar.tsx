import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const getTitleFromPath = (path: string): string => {
  switch (path) {
    case '/forecast':
      return 'Forecast de Demanda';
    case '/risk':
      return 'Scoring de Riesgo de Morosidad';
    case '/tickets':
      return 'Clasificación y Asistencia de Tickets';
    case '/':
    default:
      return 'Dashboard General';
  }
};

const Topbar = () => {
  const [apiStatus, setApiStatus] = useState<'online' | 'offline'>('offline');
  const location = useLocation();
  const title = getTitleFromPath(location.pathname);

  useEffect(() => {
    // Check API health on component mount and periodically
    const checkApiHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/health');
        if (response.ok) {
          const data = await response.json();
          if (data.status === 'ok') {
            setApiStatus('online');
            return;
          }
        }
        setApiStatus('offline');
      } catch (error) {
        setApiStatus('offline');
      }
    };

    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-gray-800">{title}</h2>
      <div className="flex items-center">
        <span className="text-sm font-medium text-gray-600 mr-2">API Status:</span>
        <div className="flex items-center">
          <div
            className={`w-3 h-3 rounded-full mr-2 ${
              apiStatus === 'online' ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span
            className={`font-semibold ${
              apiStatus === 'online' ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {apiStatus === 'online' ? 'Online' : 'Offline'}
          </span>
        </div>
      </div>
    </header>
  );
};

export default Topbar;
