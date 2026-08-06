import React, { createContext, useContext, useState, useEffect } from 'react';

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  avatarUrl?: string;
  apiKey?: string;
  createdAt: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, name?: string) => void;
  register: (name: string, email: string) => void;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const DEFAULT_USER: User = {
  id: 'usr_mv_101',
  name: 'Alex Vance',
  email: 'alex.vance@mvrag.ai',
  role: 'AI Engineer',
  avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
  apiKey: 'mv_sk_live_9924a8bf731e4f',
  createdAt: '2026-01-15T08:00:00Z',
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('mvrag_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return DEFAULT_USER;
      }
    }
    return DEFAULT_USER; // Default logged in user for immediate seamless interaction
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('mvrag_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('mvrag_user');
    }
  }, [user]);

  const login = (email: string, name?: string) => {
    const newUser: User = {
      id: `usr_${Math.random().toString(36).substr(2, 9)}`,
      name: name || email.split('@')[0] || 'User',
      email,
      role: 'Senior Developer',
      avatarUrl: DEFAULT_USER.avatarUrl,
      apiKey: `mv_sk_live_${Math.random().toString(36).substr(2, 12)}`,
      createdAt: new Date().toISOString(),
    };
    setUser(newUser);
  };

  const register = (name: string, email: string) => {
    login(email, name);
  };

  const logout = () => {
    setUser(null);
  };

  const updateUser = (data: Partial<User>) => {
    setUser((prev) => (prev ? { ...prev, ...data } : null));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
