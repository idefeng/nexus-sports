import { motion } from 'framer-motion';
import type { LucideIcon } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface MetricCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  color?: 'cyan' | 'green' | 'magenta' | 'white';
}

const colorMap = {
  cyan: 'text-cyber-cyan shadow-[0_0_15px_rgba(0,242,255,0.2)]',
  green: 'text-cyber-green shadow-[0_0_15px_rgba(57,255,20,0.2)]',
  magenta: 'text-cyber-magenta shadow-[0_0_15px_rgba(255,0,255,0.2)]',
  white: 'text-white'
};

export const MetricCard = ({ label, value, icon: Icon, color = 'cyan' }: MetricCardProps) => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className="glass-card p-6 flex items-start justify-between group cursor-default"
    >
      <div>
        <p className="text-slate-400 text-sm font-medium mb-1 uppercase tracking-wider">{label}</p>
        <h3 className="text-3xl font-bold tracking-tight text-white group-hover:text-cyber-cyan transition-colors">
          {value}
        </h3>
      </div>
      <div className={cn(
        "p-3 rounded-xl bg-white/5 transition-all group-hover:bg-white/10",
        colorMap[color]
      )}>
        <Icon size={24} />
      </div>
    </motion.div>
  );
};
