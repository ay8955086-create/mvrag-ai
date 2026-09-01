import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  Video,
  Bot,
  Search,
  BarChart3,
  History,
  Settings,
  User,
  Info,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Sun,
  Moon,
  Layers,
  Activity,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '../../contexts/ThemeContext';
import { useAuth } from '../../contexts/AuthContext';

export const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const { user } = useAuth();
  const location = useLocation();

  const navigationItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Upload Video', path: '/upload', icon: UploadCloud },
    { name: 'Video Library', path: '/videos', icon: Video },
    { name: 'Semantic Search', path: '/search', icon: Search },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
    { name: 'Query History', path: '/history', icon: History },
  ];

  const secondaryItems = [
    { name: 'Settings', path: '/settings', icon: Settings },
    { name: 'User Profile', path: '/profile', icon: User },
    { name: 'About MVRAG', path: '/about', icon: Info },
  ];

  return (
    <aside
      className={clsx(
        'relative flex flex-col h-screen glass-panel border-r border-white/10 transition-all duration-300 z-30 select-none flex-shrink-0',
        isCollapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-white/10">
        <NavLink to="/" className="flex items-center gap-3 overflow-hidden">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-cyan-400 text-white shadow-lg shadow-brand-500/30 flex-shrink-0">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          {!isCollapsed && (
            <div className="flex flex-col">
              <span className="font-extrabold text-base tracking-tight bg-gradient-to-r from-white via-slate-200 to-brand-300 bg-clip-text text-transparent">
                MVRAG AI
              </span>
              <span className="text-[10px] text-brand-400 font-semibold uppercase tracking-wider">
                Multimodal RAG
              </span>
            </div>
          )}
        </NavLink>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Main Navigation */}
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
        <div>
          {!isCollapsed && (
            <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">
              Main Menu
            </p>
          )}
          <nav className="space-y-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 group relative',
                    isActive
                      ? 'bg-brand-600/90 text-white shadow-md shadow-brand-500/20 font-semibold'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/50'
                  )}
                  title={isCollapsed ? item.name : undefined}
                >
                  <Icon className={clsx('w-4 h-4 flex-shrink-0 transition-transform group-hover:scale-110', isActive ? 'text-white' : 'text-slate-400 group-hover:text-brand-400')} />
                  {!isCollapsed && (
                    <span className="truncate flex-1">{item.name}</span>
                  )}

                </NavLink>
              );
            })}
          </nav>
        </div>

        <div>
          {!isCollapsed && (
            <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">
              Preferences
            </p>
          )}
          <nav className="space-y-1">
            {secondaryItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-all duration-200 group',
                    isActive
                      ? 'bg-slate-800 text-white font-semibold'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/40'
                  )}
                  title={isCollapsed ? item.name : undefined}
                >
                  <Icon className="w-4 h-4 flex-shrink-0 transition-transform group-hover:scale-110 text-slate-400 group-hover:text-white" />
                  {!isCollapsed && <span className="truncate">{item.name}</span>}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Footer / Controls */}
      <div className="p-3 border-t border-white/10 space-y-3">
        {/* Dark/Light mode button */}
        <button
          onClick={toggleTheme}
          className="w-full flex items-center justify-between p-2 rounded-xl text-xs text-slate-400 hover:text-white hover:bg-slate-800/50 transition-colors"
        >
          <div className="flex items-center gap-2">
            {theme === 'dark' ? <Moon className="w-4 h-4 text-indigo-400" /> : <Sun className="w-4 h-4 text-amber-400" />}
            {!isCollapsed && <span>{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</span>}
          </div>
          {!isCollapsed && (
            <div className={clsx('w-8 h-4 rounded-full p-0.5 transition-colors', theme === 'dark' ? 'bg-brand-600' : 'bg-slate-600')}>
              <div className={clsx('w-3 h-3 rounded-full bg-white transition-transform', theme === 'dark' ? 'translate-x-4' : 'translate-x-0')} />
            </div>
          )}
        </button>

        {/* User Card */}
        <div className="flex items-center gap-3 p-2 rounded-xl bg-slate-900/60 border border-slate-800">
          <img
            src={user?.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'}
            alt="Avatar"
            className="w-8 h-8 rounded-full object-cover ring-2 ring-brand-500/30 flex-shrink-0"
          />
          {!isCollapsed && (
            <div className="flex flex-col min-w-0 flex-1">
              <span className="text-xs font-semibold text-slate-200 truncate">{user?.name || 'Developer'}</span>
              <span className="text-[10px] text-slate-400 truncate">{user?.role || 'Admin'}</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};
