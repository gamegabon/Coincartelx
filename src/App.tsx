/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Cpu, 
  Eye, 
  Terminal, 
  Play, 
  Square, 
  Settings, 
  Database, 
  Zap, 
  Activity,
  ChevronRight,
  Command,
  Smartphone,
  History,
  AlertCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { OmegaAI, OmegaAction } from './services/omegaAI';

// Mock ADB connection state
interface ConnectionState {
  connected: boolean;
  target: string;
  app: string;
}

export default function App() {
  const [isGaming, setIsGaming] = useState(false);
  const [logs, setLogs] = useState<{ id: string; type: 'info' | 'ai' | 'action' | 'error'; message: string; timestamp: Date }[]>([]);
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const [connection, setConnection] = useState<ConnectionState>({
    connected: true,
    target: "192.168.1.67:33231",
    app: "com.android.launcher"
  });
  const [userInput, setUserInput] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uiMap, setUiMap] = useState<Record<string, any>>({});
  
  const logEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const addLog = (type: 'info' | 'ai' | 'action' | 'error', message: string) => {
    setLogs(prev => [...prev, {
      id: Math.random().toString(36).substr(2, 9),
      type,
      message,
      timestamp: new Date()
    }].slice(-50));
  };

  useEffect(() => {
    addLog('info', 'OMEGA v11.0 - LE ZÉNITH initialisé.');
    addLog('info', `Connecté au corps (${connection.target})`);
  }, []);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const handleAIRequest = async (prompt: string) => {
    if (!process.env.GEMINI_API_KEY) {
      addLog('error', 'Clé API Gemini manquante.');
      return;
    }

    setIsAnalyzing(true);
    addLog('info', 'Analyse cognitive en cours...');

    const omega = new OmegaAI(process.env.GEMINI_API_KEY);
    const result = await omega.analyze(prompt, screenshot || undefined, connection.app, uiMap);

    setIsAnalyzing(false);

    if (result) {
      addLog('ai', `[PENSÉE]: ${result.analyse}`);
      addLog('action', `ORDRE: ${result.action} - ${JSON.stringify(result.params)}`);
      addLog('info', `OMEGA: ${result.reponse}`);

      // Handle specific actions
      if (result.action === 'start_gaming') {
        setIsGaming(true);
        addLog('info', 'MODE AUTO-GAMER ENCLENCHÉ');
      } else if (result.action === 'learn_ui') {
        setUiMap(prev => ({ ...prev, [connection.app]: result.params.buttons }));
      }
    } else {
      addLog('error', 'Échec de la communication avec le noyau AI.');
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setScreenshot(reader.result as string);
        addLog('info', 'Nouveau flux visuel reçu.');
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-8 flex flex-col gap-6 max-w-7xl mx-auto">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center omega-glow">
              <Zap className="text-black fill-current" size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tighter uppercase mono">OMEGA <span className="text-orange-500">Zenith</span></h1>
              <p className="text-xs text-dim uppercase tracking-widest mono">v11.0 - Python Core Edition</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2 text-green-500 text-xs mono">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              PYTHON CORE: ACTIVE
            </div>
            <div className="text-[10px] text-dim mono uppercase">Target: {connection.target}</div>
          </div>
          <button 
            className="p-2 hardware-card hover:bg-white/5 transition-colors"
            onClick={() => addLog('info', 'Paramètres système ouverts.')}
          >
            <Settings size={20} className="text-dim" />
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <main className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-grow">
        
        {/* Left Column: Visual & Controls */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {/* Eyesight Viewport */}
          <div className="hardware-card relative overflow-hidden aspect-video flex flex-col bg-black">
            <div className="p-3 border-b border-white/5 flex justify-between items-center bg-white/2">
              <div className="flex items-center gap-2 text-xs mono text-dim">
                <Eye size={14} />
                EYESIGHT_FEED
              </div>
              <div className="text-[10px] mono text-dim uppercase">App: {connection.app}</div>
            </div>
            
            <div className="flex-grow relative flex items-center justify-center">
              <div className="scanline" />
              {screenshot ? (
                <img 
                  src={screenshot} 
                  alt="Device Screen" 
                  className="max-h-full object-contain"
                  referrerPolicy="no-referrer"
                />
              ) : (
                <div className="flex flex-col items-center gap-4 text-dim">
                  <Smartphone size={48} strokeWidth={1} />
                  <p className="text-xs mono uppercase tracking-widest">No visual feed detected</p>
                  <button 
                    onClick={() => fileInputRef.current?.click()}
                    className="px-4 py-2 border border-white/10 hover:border-orange-500/50 text-[10px] mono uppercase transition-all"
                  >
                    Upload Screenshot
                  </button>
                </div>
              )}
              <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                accept="image/*" 
                onChange={handleFileUpload} 
              />
            </div>

            {/* Overlay HUD */}
            <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end pointer-events-none">
              <div className="flex flex-col gap-1">
                <div className="w-24 h-1 bg-white/10 overflow-hidden">
                  <motion.div 
                    className="h-full bg-orange-500"
                    animate={{ width: ["20%", "80%", "40%", "90%"] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                </div>
                <div className="text-[8px] mono text-orange-500/70 uppercase">Processing Core Load</div>
              </div>
              <div className="text-[8px] mono text-white/30 text-right">
                LATENCY: 42ms<br />
                FPS: 60.0
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button 
              onClick={() => {
                setIsGaming(!isGaming);
                addLog('info', isGaming ? 'MODE AUTO-GAMER DÉSACTIVÉ' : 'MODE AUTO-GAMER ENCLENCHÉ');
              }}
              className={`flex flex-col items-center justify-center gap-2 p-4 hardware-card transition-all ${isGaming ? 'border-orange-500 bg-orange-500/10' : 'hover:bg-white/5'}`}
            >
              {isGaming ? <Square size={20} className="text-orange-500" /> : <Play size={20} className="text-orange-500" />}
              <span className="text-[10px] mono uppercase font-bold">{isGaming ? 'Stop Loop' : 'Start Loop'}</span>
            </button>

            <button 
              onClick={() => handleAIRequest("Analyse et joue.")}
              className="flex flex-col items-center justify-center gap-2 p-4 hardware-card hover:bg-white/5 transition-all"
            >
              <Cpu size={20} className="text-blue-400" />
              <span className="text-[10px] mono uppercase font-bold">AI Think</span>
            </button>

            <button 
              onClick={() => addLog('info', 'UI Map Refresh requested.')}
              className="flex flex-col items-center justify-center gap-2 p-4 hardware-card hover:bg-white/5 transition-all"
            >
              <Database size={20} className="text-purple-400" />
              <span className="text-[10px] mono uppercase font-bold">Sync Map</span>
            </button>

            <button 
              onClick={() => setScreenshot(null)}
              className="flex flex-col items-center justify-center gap-2 p-4 hardware-card hover:bg-white/5 transition-all"
            >
              <History size={20} className="text-dim" />
              <span className="text-[10px] mono uppercase font-bold">Clear Feed</span>
            </button>
          </div>
        </div>

        {/* Right Column: Console & Input */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* Console */}
          <div className="hardware-card flex-grow flex flex-col min-h-[400px] bg-black/40">
            <div className="p-3 border-b border-white/5 flex items-center gap-2 text-xs mono text-dim bg-white/2">
              <Terminal size={14} />
              OMEGA_COGNITIVE_LOGS
            </div>
            
            <div className="flex-grow p-4 overflow-y-auto font-mono text-[11px] space-y-2 scrollbar-thin">
              <AnimatePresence initial={false}>
                {logs.map((log) => (
                  <motion.div 
                    key={log.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex gap-2"
                  >
                    <span className="text-white/20 shrink-0">[{log.timestamp.toLocaleTimeString([], { hour12: false })}]</span>
                    <span className={`
                      ${log.type === 'ai' ? 'text-orange-400' : ''}
                      ${log.type === 'action' ? 'text-blue-400 font-bold' : ''}
                      ${log.type === 'error' ? 'text-red-500' : ''}
                      ${log.type === 'info' ? 'text-dim' : ''}
                    `}>
                      {log.type === 'ai' && <span className="mr-1">🧠</span>}
                      {log.type === 'action' && <span className="mr-1">🤖</span>}
                      {log.type === 'error' && <AlertCircle size={10} className="inline mr-1" />}
                      {log.message}
                    </span>
                  </motion.div>
                ))}
              </AnimatePresence>
              <div ref={logEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-white/5 bg-white/2">
              <form 
                onSubmit={(e) => {
                  e.preventDefault();
                  if (userInput.trim()) {
                    addLog('info', `MAÎTRE: ${userInput}`);
                    handleAIRequest(userInput);
                    setUserInput("");
                  }
                }}
                className="relative"
              >
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-orange-500">
                  <ChevronRight size={16} />
                </div>
                <input 
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder={isAnalyzing ? "Processing..." : "Enter command for OMEGA..."}
                  disabled={isAnalyzing}
                  className="w-full bg-black/60 border border-white/10 rounded p-2 pl-8 text-xs mono focus:border-orange-500 outline-none transition-all disabled:opacity-50"
                />
                <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                  <span className="text-[10px] text-white/20 mono hidden md:block">ENTER TO SEND</span>
                  <Command size={12} className="text-white/20" />
                </div>
              </form>
            </div>
          </div>

          {/* System Stats */}
          <div className="hardware-card p-4 space-y-4">
            <div className="flex items-center gap-2 text-xs mono text-dim">
              <Activity size={14} />
              SYSTEM_VITALS
            </div>
            
            <div className="space-y-3">
              <div className="space-y-1">
                <div className="flex justify-between text-[10px] mono uppercase">
                  <span>AI Core Temperature</span>
                  <span className="text-orange-500">42°C</span>
                </div>
                <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-orange-500 w-[42%]" />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[10px] mono uppercase">
                  <span>Memory Matrix Usage</span>
                  <span className="text-blue-400">1.2 GB / 16 GB</span>
                </div>
                <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-400 w-[15%]" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="p-2 bg-white/2 border border-white/5 rounded">
                  <div className="text-[8px] text-dim uppercase mono">API Keys</div>
                  <div className="text-xs mono">4 / 4 ACTIVE</div>
                </div>
                <div className="p-2 bg-white/2 border border-white/5 rounded">
                  <div className="text-[8px] text-dim uppercase mono">Uptime</div>
                  <div className="text-xs mono">04:12:33</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer / Status Bar */}
      <footer className="border-t border-white/10 pt-4 flex justify-between items-center text-[10px] mono text-dim uppercase tracking-widest">
        <div className="flex gap-6">
          <span>ADB_STATUS: OK</span>
          <span>GEMINI_LINK: ESTABLISHED</span>
          <span>ENCRYPTION: AES-256</span>
        </div>
        <div className="hidden md:block">
          © 2026 OMEGA ZENITH COMMAND CENTER
        </div>
      </footer>
    </div>
  );
}
