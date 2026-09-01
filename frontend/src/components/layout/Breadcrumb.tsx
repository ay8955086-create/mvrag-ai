import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

export const Breadcrumb: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  const routeNameMap: Record<string, string> = {
    upload: 'Upload Video',
    videos: 'Video Library',
    search: 'Semantic Search',
    analytics: 'Analytics',
    history: 'Query History',
    settings: 'Settings',
    profile: 'User Profile',
    about: 'About MVRAG',
    processing: 'Processing Status',
  };

  return (
    <nav className="flex items-center gap-1.5 text-xs text-slate-400 select-none">
      <Link to="/" className="flex items-center gap-1 hover:text-white transition-colors">
        <Home className="w-3.5 h-3.5 text-brand-400" />
        <span>Dashboard</span>
      </Link>
      {pathnames.map((value, index) => {
        const to = `/${pathnames.slice(0, index + 1).join('/')}`;
        const isLast = index === pathnames.length - 1;
        const displayName = routeNameMap[value] || (isNaN(Number(value)) ? value : `Item #${value}`);

        return (
          <React.Fragment key={to}>
            <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
            {isLast ? (
              <span className="font-semibold text-slate-200 capitalize">{displayName}</span>
            ) : (
              <Link to={to} className="hover:text-white transition-colors capitalize">
                {displayName}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
