import { useEffect, useState } from 'react';
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { activityService } from '../services/api';
import type { MonthlyTrend, TypeDistribution } from '../types';

export const Stats = () => {
  const { t } = useTranslation();
  const [trend, setTrend] = useState<MonthlyTrend[]>([]);
  const [dist, setDist] = useState<TypeDistribution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [trendData, distData] = await Promise.all([
          activityService.getStatsTrend(),
          activityService.getStatsDistribution()
        ]);
        setTrend(trendData.trends || []);
        setDist(distData.distribution || []);
      } catch (error) {
        console.error('Failed to fetch stats data', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return null;

  const COLORS = ['#00F2FF', '#39FF14', '#FF00FF', '#FFFF00', '#FF3131'];

  return (
    <div className="space-y-10">
      <header>
        <motion.h1 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-4xl font-black text-white tracking-tighter"
        >
          {t('stats.header')} <span className="text-cyber-green italic">{t('stats.insights')}</span>
        </motion.h1>
        <p className="text-slate-500 font-medium mt-1 uppercase tracking-widest text-sm">{t('stats.sub')}</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trend Chart */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-8 min-h-[400px]"
        >
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white tracking-tight uppercase">{t('stats.monthly_progression')}</h3>
            <p className="text-slate-500 text-sm tracking-wide">{t('stats.monthly_sub')}</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trend}>
                <defs>
                  <linearGradient id="colorDist" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00F2FF" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#00F2FF" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                <XAxis 
                  dataKey="month" 
                  stroke="#64748b" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false}
                />
                <YAxis 
                  stroke="#64748b" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false} 
                  tickFormatter={(val) => `${val}k`}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#121216', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                  itemStyle={{ color: '#00F2FF' }}
                />
                <Area 
                  type="monotone" 
                  dataKey="distance_km" 
                  stroke="#00F2FF" 
                  strokeWidth={3}
                  fillOpacity={1} 
                  fill="url(#colorDist)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Distribution Chart */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-8 min-h-[400px]"
        >
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white tracking-tight uppercase">{t('stats.activity_profile')}</h3>
            <p className="text-slate-500 text-sm tracking-wide">{t('stats.activity_sub')}</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={dist}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={8}
                  dataKey="count"
                  nameKey="type"
                >
                  {dist.map((_entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#121216', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-wrap justify-center gap-4 mt-4">
              {dist.map((d, i) => (
                <div key={d.type} className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-tighter">{d.type}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
