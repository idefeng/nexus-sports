import { useTranslation } from 'react-i18next';
import { Languages } from 'lucide-react';
import { motion } from 'framer-motion';

export const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const nextLng = i18n.language.startsWith('en') ? 'zh' : 'en';
    i18n.changeLanguage(nextLng);
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-slate-400 hover:text-cyber-cyan hover:border-cyber-cyan/30 transition-all text-xs font-bold uppercase tracking-widest"
    >
      <Languages size={14} />
      <span>{i18n.language.startsWith('en') ? 'English' : '中文'}</span>
    </motion.button>
  );
};
