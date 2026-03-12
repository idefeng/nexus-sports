import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Database, Info, Globe } from 'lucide-react';

export const SettingsPage = () => {
  const { t, i18n } = useTranslation();

  const isZh = i18n.language.startsWith('zh');

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
    <div className="max-w-2xl mx-auto space-y-10">
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
    </div>
  );
};
