import React, { useState, useEffect } from 'react';
import { Search, LayoutDashboard, Map, Smartphone, Users, AlertTriangle, Activity, X } from 'lucide-react';
import { NavView } from './Sidebar';
import { SimulationScenarioId } from '../../types/simulation';
import { SIMULATION_SCENARIOS } from '../../simulation/scenarios';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectView: (view: NavView) => void;
  onSelectScenario: (scenarioId: SimulationScenarioId) => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onSelectView,
  onSelectScenario,
}) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery('');
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const navigationOptions = [
    { label: 'Go to Command Center', view: 'command-center', icon: LayoutDashboard },
    { label: 'View Live Operations GIS Map', view: 'live-ops', icon: Map },
    { label: 'Open Worker Mobile Experience', view: 'worker-safety', icon: Smartphone },
    { label: 'Open Team Safety Matrix', view: 'team-safety', icon: Users },
    { label: 'Open Alert Queue', view: 'alerts', icon: AlertTriangle },
    { label: 'View System Health', view: 'system-health', icon: Activity },
  ];

  const scenarioOptions = Object.values(SIMULATION_SCENARIOS);

  const filteredNav = navigationOptions.filter((n) => n.label.toLowerCase().includes(query.toLowerCase()));
  const filteredScenarios = scenarioOptions.filter(
    (s) => s.title.toLowerCase().includes(query.toLowerCase()) || s.description.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-start justify-center pt-20 p-4">
      <div className="bg-[#121826] border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-150">
        {/* Search Input Bar */}
        <div className="flex items-center px-4 border-b border-slate-800">
          <Search className="w-5 h-5 text-slate-400 mr-3" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or search scenario... (e.g., Train Approaching, Emergency)"
            className="w-full bg-transparent py-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
          />
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Command List Container */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-4">
          {/* Navigation Section */}
          {filteredNav.length > 0 && (
            <div>
              <div className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-slate-400">Navigation</div>
              <div className="space-y-1 mt-1">
                {filteredNav.map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.view}
                      onClick={() => {
                        onSelectView(item.view as NavView);
                        onClose();
                      }}
                      className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition"
                    >
                      <Icon className="w-4 h-4 text-cyan-400" />
                      <span>{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Simulation Scenarios Section */}
          {filteredScenarios.length > 0 && (
            <div>
              <div className="px-3 py-1 text-[10px] font-mono uppercase tracking-wider text-slate-400">
                Trigger Simulation Scenario
              </div>
              <div className="space-y-1 mt-1">
                {filteredScenarios.map((sc) => (
                  <button
                    key={sc.id}
                    onClick={() => {
                      onSelectScenario(sc.id);
                      onClose();
                    }}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800 transition group"
                  >
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300">{sc.title}</div>
                    <div className="text-[11px] text-slate-400 line-clamp-1">{sc.description}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {filteredNav.length === 0 && filteredScenarios.length === 0 && (
            <div className="py-8 text-center text-xs text-slate-400">No commands matching &quot;{query}&quot;</div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 border-t border-slate-800 bg-[#090D16] flex justify-between items-center text-[10px] text-slate-400 font-mono">
          <span>Use ARROW keys to navigate</span>
          <span>Press ESC to exit</span>
        </div>
      </div>
    </div>
  );
};
