import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Layout/Sidebar';
import Topbar from './components/Layout/Topbar';
import DashboardPage from './pages/DashboardPage';
import ForecastPage from './pages/ForecastPage';
import RiskPage from './pages/RiskPage';
import TicketsPage from './pages/TicketsPage';

function App() {
  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/forecast" element={<ForecastPage />} />
            <Route path="/risk" element={<RiskPage />} />
            <Route path="/tickets" element={<TicketsPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
