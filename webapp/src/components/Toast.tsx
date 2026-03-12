import { useState, useEffect, useCallback, createContext, useContext, type ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

interface ToastContextType {
  success: (message: string) => void;
  error: (message: string) => void;
  info: (message: string) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) throw new Error('useToast must be used within ToastProvider');
  return context;
};

let nextId = 0;

export const ToastProvider = ({ children }: { children: ReactNode }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((type: ToastType, message: string) => {
    const id = nextId++;
    setToasts(prev => [...prev, { id, type, message }]);
  }, []);

  const removeToast = useCallback((id: number) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  const contextValue: ToastContextType = {
    success: (msg) => addToast('success', msg),
    error: (msg) => addToast('error', msg),
    info: (msg) => addToast('info', msg),
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      <div className="fixed bottom-6 right-6 z-[10000] space-y-3">
        <AnimatePresence>
          {toasts.map(toast => (
            <ToastItem key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
};

const ICONS = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
};

const COLORS = {
  success: 'border-cyber-green bg-cyber-green/5 text-cyber-green',
  error: 'border-red-500 bg-red-500/5 text-red-400',
  info: 'border-cyber-cyan bg-cyber-cyan/5 text-cyber-cyan',
};

const ToastItem = ({ toast, onClose }: { toast: Toast; onClose: () => void }) => {
  const Icon = ICONS[toast.type];

  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <motion.div
      initial={{ x: 100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 100, opacity: 0 }}
      className={`glass-card flex items-center gap-3 px-5 py-3 border-l-4 min-w-[280px] ${COLORS[toast.type]}`}
    >
      <Icon size={18} />
      <span className="text-sm font-medium text-white flex-1">{toast.message}</span>
      <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors">
        <X size={14} />
      </button>
    </motion.div>
  );
};
