import React from 'react';
import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from '../views/Dashboard';
import Reports from '../views/Reports';
import Tutorial from '../views/Tutorial';

const queryClient = new QueryClient();

const NavBar: React.FC = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-4 py-2 rounded-md text-sm font-semibold transition-colors ${
      isActive
        ? 'bg-indigo-600 text-white'
        : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
    }`;

  return (
    <header className="bg-white/80 dark:bg-slate-900/70 backdrop-blur sticky top-0 z-20 border-b border-slate-200 dark:border-slate-800">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl font-bold text-slate-800 dark:text-slate-100">Sleuth Dashboard</span>
        </div>
        <nav className="flex items-center gap-2">
          <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
          <NavLink to="/reports" className={linkClass}>Reports</NavLink>
          <NavLink to="/tutorial" className={linkClass}>Tutorial</NavLink>
        </nav>
      </div>
    </header>
  );
};

const AppRouter: React.FC = () => {
  // Use root basename for Vercel deployment to avoid 404 on client routes like /reports
  // If you later deploy under a subpath (e.g., GitHub Pages), consider using an env var:
  // const basename = import.meta.env.VITE_BASE_PATH || '/';
  const basename = '/';
  
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter basename={basename}>
        <NavBar />
        <main className="max-w-6xl mx-auto px-4 py-6">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/tutorial" element={<Tutorial />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
        <footer className="text-center p-6 text-sm text-slate-500 dark:text-slate-400">
          <p>Bias analysis dashboard (MVP). Charts powered by Plotly. Data mocked.</p>
        </footer>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default AppRouter;
