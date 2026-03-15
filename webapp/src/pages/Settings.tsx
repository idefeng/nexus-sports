import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Database, Info, Globe, AlertTriangle, Trash2, Loader2 } from 'lucide-react';
import { activityService } from '../services/api';
import { useToast } from '../components/Toast';

export const SettingsPage = () => {
  const { t, i18n } = useTranslation();
  const toast = useToast();
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [confirmValue, setConfirmValue] = useState('');
  const [isClearing, setIsClearing] = useState(false);

  const isZh = i18n.language.startsWith('zh');
  const CONFIRM_TEXT = 'nexus-sports';

  const handleClearAll = async () => {
    if (confirmValue !== CONFIRM_TEXT) return;
    setIsClearing(true);
    try {
      await activityService.clearAllActivities();
      toast.success(isZh ? '所有数据已成功清除' : 'All data cleared successfully');
      setShowClearConfirm(false);
      setConfirmValue('');
    } catch (e) {
      toast.error(isZh ? '清除失败，请稍后重试' : 'Clear failed, please try again');
    } finally {
      setIsClearing(false);
    }
  };

  const settingGroups = [
    {
      icon: Globe,
      title: isZh ? '语言设置' : 'Language',
      description: isZh ? '选择界面显示语言' : 'Select interface language',
      content: (
        <div className="flex gap-3 mt-3">
          {(['en', 'zh'] as const).map(lang => (
            <button
              key={lang}
              onClick={() => i18n.changeLanguage(lang)}
              className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                i18n.language.startsWith(lang)
                  ? 'bg-cyber-cyan text-black'
                  : 'bg-white/5 text-slate-400 hover:bg-white/10'
              }`}
            >
              {lang === 'en' ? 'English' : '中文'}
            </button>
          ))}
        </div>
      ),
    },
    {
      icon: Database,
      title: isZh ? '数据管理' : 'Data Management',
      description: isZh ? '管理本地运动数据' : 'Manage local activity data',
      content: (
        <div className="mt-3 space-y-3">
          <div className="flex items-center justify-between bg-white/5 px-4 py-3 rounded-xl">
            <div>
              <p className="text-sm font-bold text-white">{isZh ? '数据目录' : 'Data Directory'}</p>
              <p className="text-xs text-slate-500 font-mono">data/</p>
            </div>
          </div>
          <div className="flex items-center justify-between bg-white/5 px-4 py-3 rounded-xl">
            <div>
              <p className="text-sm font-bold text-white">{isZh ? '数据库' : 'Database'}</p>
              <p className="text-xs text-slate-500 font-mono">data/nexus_sports.db (SQLite)</p>
            </div>
          </div>
        </div>
      ),
    },
    {
      icon: AlertTriangle,
      title: isZh ? '危险区域' : 'Danger Zone',
      description: isZh ? '涉及数据删除的操作，请谨慎执行' : 'Actions involving data deletion, proceed with caution',
      content: (
        <div className="mt-4">
          <button 
            onClick={() => setShowClearConfirm(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-500/10 text-red-500 border border-red-500/20 text-sm font-bold hover:bg-red-500/20 transition-all group"
          >
            <Trash2 size={16} className="group-hover:animate-bounce" />
            {isZh ? '清除所有运动数据' : 'Clear All Activity Data'}
          </button>
          <p className="text-[10px] text-slate-600 mt-2 italic">
            {isZh ? '* 此操作将物理删除所有数据库记录及原始备份文件，不可恢复。' : '* This will physically delete all DB records and raw backups, irreversible.'}
          </p>
        </div>
      ),
    },
    {
      icon: Info,
      title: isZh ? '关于 Nexus Sports' : 'About Nexus Sports',
      description: isZh ? '版本信息和技术栈' : 'Version and technology stack',
      content: (
        <div className="mt-3 space-y-2">
          <p className="text-xs font-mono text-slate-500">
            <span className="text-cyber-cyan">Backend</span> — FastAPI · SQLAlchemy · Python
          </p>
          <p className="text-xs font-mono text-slate-500">
            <span className="text-cyber-green">Frontend</span> — React · Vite · TailwindCSS · Recharts
          </p>
          <p className="text-xs font-mono text-slate-500">
            <span className="text-purple-400">Data</span> — FIT · GPX · Polyline · Leaflet
          </p>
          <div className="mt-4 pt-4 border-t border-white/5">
            <p className="text-[10px] text-slate-600 font-mono uppercase tracking-widest">
              Nexus Sports v1.0 • MIT License
            </p>
          </div>
        </div>
      ),
    },
  ];

  return (
    <div className="max-w-2xl mx-auto space-y-10 relative">
      <header>
        <motion.h1
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-4xl font-black text-white tracking-tighter"
        >
          {t('common.settings')}
        </motion.h1>
        <p className="text-slate-500 font-medium mt-1 uppercase tracking-widest text-sm">
          {isZh ? '应用配置与数据管理' : 'Application configuration & data management'}
        </p>
      </header>

      <div className="space-y-6">
        {settingGroups.map((group, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="glass-card p-6"
          >
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center flex-shrink-0">
                <group.icon size={18} className="text-cyber-cyan" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white">{group.title}</h3>
                <p className="text-sm text-slate-500">{group.description}</p>
                {group.content}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Confirmation Modal */}
      <AnimatePresence>
        {showClearConfirm && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-[9999] p-4">
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass-card max-w-md w-full p-8 border border-red-500/30 shadow-[0_0_50px_rgba(239,68,68,0.1)]"
            >
              <div className="flex items-center gap-3 text-red-500 mb-4">
                <AlertTriangle size={24} />
                <h3 className="text-xl font-black italic uppercase tracking-tighter">{isZh ? '彻底清除确认' : 'Wipe Data Confirmation'}</h3>
              </div>
              
              <p className="text-slate-400 text-sm mb-6 leading-relaxed">
                {isZh 
                  ? '您正在执行全量删除操作。这将清空所有运动活动、导入记录以及原始文件备份。请输入下方提示文字以确认执行：'
                  : 'You are about to wipe ALL activity data, records, and raw backups. This is irreversible. Please type the following to confirm:'}
              </p>

              <div className="bg-white/5 p-3 rounded-lg mb-6 flex items-center justify-center select-none pointer-events-none">
                <span className="text-cyber-cyan font-mono font-bold text-lg tracking-[0.3em]">{CONFIRM_TEXT}</span>
              </div>

              <input 
                type="text"
                value={confirmValue}
                onChange={e => setConfirmValue(e.target.value)}
                placeholder={isZh ? '在这里输入确认文字...' : 'Type confirmation here...'}
                className="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-red-500 transition-colors mb-6 font-mono"
              />

              <div className="flex gap-3">
                <button 
                  onClick={() => { setShowClearConfirm(false); setConfirmValue(''); }}
                  className="flex-1 px-4 py-3 rounded-xl bg-white/5 text-slate-400 text-sm font-bold hover:bg-white/10 transition-colors"
                >
                  {isZh ? '取消' : 'Cancel'}
                </button>
                <button 
                  disabled={confirmValue !== CONFIRM_TEXT || isClearing}
                  onClick={handleClearAll}
                  className="flex-[2] px-4 py-3 rounded-xl bg-red-500 text-white text-sm font-black uppercase italic tracking-widest disabled:opacity-30 disabled:cursor-not-allowed hover:bg-red-600 transition-all flex items-center justify-center gap-2"
                >
                  {isClearing ? <Loader2 className="animate-spin" size={18} /> : <Trash2 size={18} />}
                  {isZh ? '立即清除' : 'Wipe Now'}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};
