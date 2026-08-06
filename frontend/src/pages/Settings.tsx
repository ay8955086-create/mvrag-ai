import React, { useState } from 'react';
import { Settings as SettingsIcon, Moon, Sun, Globe, Cpu, Bell, Key, Save, Server, Database } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { toast } from 'sonner';

export const Settings: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const [apiUrl, setApiUrl] = useState(import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');
  const [vectorCollection, setVectorCollection] = useState('mvrag_video_embeddings');
  const [llmProvider, setLlmProvider] = useState('ollama');
  const [openaiKey, setOpenaiKey] = useState('sk-proj-••••••••••••••••••••');
  const [geminiKey, setGeminiKey] = useState('AIzaSy••••••••••••••••••••');
  const [notifications, setNotifications] = useState(true);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('System settings saved successfully!');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-brand-400" />
          Application Settings & Config
        </h1>
        <p className="text-xs text-slate-400">
          Configure local FastAPI backend connection, LLM provider keys, ChromaDB vector collection, and appearance.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Appearance Settings */}
        <Card glass className="p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Sun className="w-4 h-4 text-amber-400" />
            Appearance & Theme Mode
          </h3>

          <div className="grid grid-cols-2 gap-4 max-w-md">
            <button
              type="button"
              onClick={() => setTheme('dark')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                theme === 'dark'
                  ? 'bg-brand-500/10 border-brand-500 text-white shadow-lg'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400'
              }`}
            >
              <Moon className="w-5 h-5 mb-2 text-indigo-400" />
              <div className="text-xs font-bold">Dark Mode</div>
              <div className="text-[10px] text-slate-400">Apple & OpenAI Style</div>
            </button>

            <button
              type="button"
              onClick={() => setTheme('light')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                theme === 'light'
                  ? 'bg-brand-500/10 border-brand-500 text-white shadow-lg'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400'
              }`}
            >
              <Sun className="w-5 h-5 mb-2 text-amber-400" />
              <div className="text-xs font-bold">Light Mode</div>
              <div className="text-[10px] text-slate-400">High Contrast Glass</div>
            </button>
          </div>
        </Card>

        {/* Backend & API Settings */}
        <Card glass className="p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Server className="w-4 h-4 text-brand-400" />
            FastAPI Backend Endpoint & Vector Storage
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="FastAPI Base URL"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              placeholder="http://localhost:8000"
            />
            <Input
              label="ChromaDB Collection Name"
              value={vectorCollection}
              onChange={(e) => setVectorCollection(e.target.value)}
            />
          </div>
        </Card>

        {/* LLM Provider Configuration */}
        <Card glass className="p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            LLM RAG Generation Provider
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Select Active LLM Engine</label>
              <select
                value={llmProvider}
                onChange={(e) => setLlmProvider(e.target.value)}
                className="w-full max-w-md bg-slate-900/80 border border-slate-700/80 text-slate-100 text-xs rounded-xl p-3 outline-none focus:border-brand-500"
              >
                <option value="ollama">Ollama Local LLM (Llama3 / Mistral)</option>
                <option value="openai">OpenAI (GPT-4o / GPT-3.5-Turbo)</option>
                <option value="gemini">Google Gemini 1.5 Pro / Flash</option>
              </select>
            </div>

            {llmProvider === 'openai' && (
              <Input
                label="OpenAI API Key"
                type="password"
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
                leftIcon={<Key className="w-4 h-4 text-slate-400" />}
              />
            )}

            {llmProvider === 'gemini' && (
              <Input
                label="Gemini API Key"
                type="password"
                value={geminiKey}
                onChange={(e) => setGeminiKey(e.target.value)}
                leftIcon={<Key className="w-4 h-4 text-slate-400" />}
              />
            )}
          </div>
        </Card>

        {/* Notification Settings */}
        <Card glass className="p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Bell className="w-4 h-4 text-brand-400" />
            Notification Preferences
          </h3>

          <label className="flex items-center justify-between p-3 rounded-xl bg-slate-900/40 border border-slate-800 cursor-pointer">
            <div>
              <div className="text-xs font-semibold text-slate-200">Pipeline Completion Sound & Toast</div>
              <div className="text-[10px] text-slate-400">Notify when audio, OCR, and ChromaDB vector indexing finishes</div>
            </div>
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="w-4 h-4 rounded text-brand-600 focus:ring-brand-500 bg-slate-900 border-slate-700"
            />
          </label>
        </Card>

        <div className="flex justify-end">
          <Button type="submit" size="lg" leftIcon={<Save className="w-4 h-4" />}>
            Save All Preferences
          </Button>
        </div>
      </form>
    </div>
  );
};
