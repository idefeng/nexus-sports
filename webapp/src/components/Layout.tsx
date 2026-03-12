import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  BarChart3, 
  Map as MapIcon, 
  Upload, 
  Settings, 
  Activity
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { LanguageSwitcher } from './LanguageSwitcher';

export const Layout = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const { t } = useTranslation();

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: t('common.dashboard') },
    { path: '/stats', icon: BarChart3, label: t('common.statistics') },
    { path: '/explorer', icon: MapIcon, label: t('common.explorer') },
    { path: '/import', icon: Upload, label: t('common.import') },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-obsidian-light border-r border-white/5 flex flex-col">
        <div className="p-8 flex items-center gap-3">
          <div className="w-10 h-10 bg-cyber-cyan rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(0,242,255,0.4)]">
            <Activity className="text-black" size={24} />
          </div>
          <span className="text-xl font-black tracking-tighter text-white uppercase italic">Nexus<span className="text-cyber-cyan">Sports</span></span>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link key={item.path} to={item.path}>
                <div className={`
                  flex items-center justify-between px-4 py-3 rounded-xl transition-all group
                  ${isActive 
                    ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20' 
                    : 'text-slate-400 hover:text-white hover:bg-white/5'}
                `}>
                  <div className="flex items-center gap-3">
                    <item.icon size={20} className={isActive ? 'animate-pulse' : ''} />
                    <span className="font-semibold">{item.label}</span>
                  </div>
                  {isActive && <motion.div layoutId="activeDot" className="w-1.5 h-1.5 rounded-full bg-cyber-cyan shadow-[0_0_8px_rgba(0,242,255,1)]" />}
                </div>
              </Link>
            );
          })}
        </nav>

        <div className="p-6 space-y-4">
          <LanguageSwitcher />
          <button className="flex items-center gap-3 text-slate-500 hover:text-white transition-colors">
            <Settings size={20} />
            <span className="font-medium">{t('common.settings')}</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};
