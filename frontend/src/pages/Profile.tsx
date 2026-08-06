import React, { useState } from 'react';
import { User as UserIcon, Mail, Key, Shield, Copy, Check, Save } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { toast } from 'sonner';

export const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();

  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [role, setRole] = useState(user?.role || '');
  const [copiedKey, setCopiedKey] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    updateUser({ name, email, role });
    toast.success('Profile information updated.');
  };

  const handleCopyKey = () => {
    if (user?.apiKey) {
      navigator.clipboard.writeText(user.apiKey);
      setCopiedKey(true);
      toast.success('API key copied to clipboard.');
      setTimeout(() => setCopiedKey(false), 2000);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
          <UserIcon className="w-6 h-6 text-brand-400" />
          User Profile & Access Credentials
        </h1>
        <p className="text-xs text-slate-400">Manage account information and developer API access tokens.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Avatar Sidebar */}
        <Card glass className="p-6 text-center space-y-4 flex flex-col items-center justify-center">
          <img
            src={user?.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'}
            alt="Avatar"
            className="w-24 h-24 rounded-full object-cover ring-4 ring-brand-500/40 shadow-xl"
          />
          <div>
            <h2 className="text-base font-bold text-slate-100">{user?.name}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{user?.role}</p>
          </div>
          <div className="pt-3 border-t border-white/5 w-full text-[10px] font-mono text-slate-500">
            User ID: {user?.id}
          </div>
        </Card>

        {/* Profile Form */}
        <div className="md:col-span-2 space-y-6">
          <form onSubmit={handleSave} className="space-y-6">
            <Card glass className="p-6 space-y-4">
              <h3 className="text-sm font-bold text-slate-100">Personal Information</h3>

              <Input
                label="Full Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                leftIcon={<UserIcon className="w-4 h-4" />}
              />

              <Input
                label="Email Address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                leftIcon={<Mail className="w-4 h-4" />}
              />

              <Input
                label="Role / Title"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                leftIcon={<Shield className="w-4 h-4" />}
              />

              <div className="flex justify-end pt-2">
                <Button type="submit" size="sm" leftIcon={<Save className="w-4 h-4" />}>
                  Save Changes
                </Button>
              </div>
            </Card>
          </form>

          {/* API Key Credentials */}
          <Card glass className="p-6 space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Key className="w-4 h-4 text-brand-400" />
              Developer REST API Key
            </h3>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-between font-mono text-xs text-brand-300">
              <span className="truncate">{user?.apiKey}</span>
              <button
                onClick={handleCopyKey}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors ml-2"
              >
                {copiedKey ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
            <p className="text-[10px] text-slate-400">
              Use this bearer key to authorize custom programmatic calls to the FastAPI endpoint.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
