import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Home } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <Card glass className="max-w-md w-full p-8 text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-rose-500/10 text-rose-400 mx-auto flex items-center justify-center">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h1 className="text-4xl font-extrabold text-slate-100 font-mono">404</h1>
        <h2 className="text-base font-bold text-slate-200">Page Not Found</h2>
        <p className="text-xs text-slate-400">
          The route you are looking for does not exist or has been moved.
        </p>
        <Button onClick={() => navigate('/')} leftIcon={<Home className="w-4 h-4" />}>
          Return to Dashboard
        </Button>
      </Card>
    </div>
  );
};
