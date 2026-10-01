import React from 'react';
import {
  LayoutDashboard,
  Map,
  Users,
  MapPin,
  TrainTrack,
  BellRing,
  ShieldAlert,
  BarChart3,
  Activity,
  FileCheck2,
  Settings,
  Shield,
  Smartphone,
} from 'lucide-react';

export type NavView =
  | 'command-center'
  | 'live-ops'
  | 'worker-safety'
  | 'team-safety'
  | 'work-zones'
  | 'trains'
  | 'alerts'
  | 'near-misses'
  | 'analytics'
  | 'system-health'
  | 'audit-events'
  | 'settings';

interface SidebarProps {
  currentView: NavView;
  onSelectView: (view: NavView) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  unacknowledgedAlertCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  onSelectView,
  collapsed,
  unacknowledgedAlertCount,
}) => {
  const navItems = [
    { id: 'command-center', label: 'Command Center', icon: LayoutDashboard },
    { id: 'live-ops', label: 'Live Operations Map', icon: Map },
    { id: 'worker-safety', label: 'Worker Mobile View', icon: Smartphone },
    { id: 'team-safety', label: 'Team Safety Matrix', icon: Users },
    { id: 'work-zones', label: 'Work Zones', icon: MapPin },
    { id: 'trains', label: 'Train Movements', icon: TrainTrack },
    {
      id: 'alerts',
      label: 'Alert Queue',
      icon: BellRing,
      badge: unacknowledgedAlertCount > 0 ? unacknowledgedAlertCount : undefined,
    },
    { id: 'near-misses', label: 'Near-Miss Intelligence', icon: ShieldAlert },
    { id: 'analytics', label: 'Safety Analytics', icon: BarChart3 },
    { id: 'system-health', label: 'System & Hardware Health', icon: Activity },
    { id: 'audit-events', label: 'Audit Trail & Events', icon: FileCheck2 },
    { id: 'settings', label: 'Safety Parameters', icon: Settings },
  ];

  return (
    <aside
      className={`bg-[#0D1322] border-r border-slate-800 transition-all duration-300 flex flex-col z-20 ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center border-b border-slate-800 space-x-3">
        <div className="p-2 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-md shadow-cyan-900/30">
          <Shield className="w-5 h-5" />
        </div>
        {!collapsed && (
          <div className="flex flex-col">
            <span className="font-bold text-sm tracking-wide text-white font-mono">DOST GUARDIAN</span>
            <span className="text-[10px] text-cyan-400 font-mono tracking-widest">SAFETY COMMAND 2.0</span>
          </div>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectView(item.id as NavView)}
              className={`w-full flex items-center px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              } ${collapsed ? 'justify-center' : 'justify-between'}`}
              title={collapsed ? item.label : undefined}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                {!collapsed && <span>{item.label}</span>}
              </div>

              {!collapsed && item.badge && (
                <span className="px-2 py-0.5 text-[10px] font-mono font-bold bg-red-500 text-white rounded-full animate-pulse">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer / System Status */}
      {!collapsed && (
        <div className="p-3 border-t border-slate-800 bg-[#090D16]/50">
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span className="flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>SIMULATION ACTIVE</span>
            </span>
            <span className="text-cyan-400">v2.0.0</span>
          </div>
        </div>
      )}
    </aside>
  );
};
