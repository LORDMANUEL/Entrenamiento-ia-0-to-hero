import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BrainCircuit, ShieldAlert, MessageSquareText } from 'lucide-react';

const navItems = [
  { to: '/', text: 'Dashboard', icon: LayoutDashboard },
  { to: '/forecast', text: 'Forecast Demanda', icon: BrainCircuit },
  { to: '/risk', text: 'Riesgo de Morosidad', icon: ShieldAlert },
  { to: '/tickets', text: 'Tickets IA', icon: MessageSquareText },
];

const Sidebar = () => {
  return (
    <aside className="w-64 flex-shrink-0 bg-white border-r border-gray-200 flex flex-col shadow-lg">
      <div className="h-16 flex items-center justify-center border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-800">AI Suite</h1>
      </div>
      <nav className="flex-grow p-4">
        <ul>
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center px-4 py-3 my-1 rounded-lg transition-all duration-200 ease-in-out
                  ${isActive
                    ? 'bg-blue-100 text-blue-600 shadow-inner'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                <span className="font-medium">{item.text}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">© 2024 AI Business Suite</p>
      </div>
    </aside>
  );
};

export default Sidebar;
