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
  Area,
  BarChart,
  Bar
} from 'recharts';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { useStatsTrend, useStatsDistribution } from '../hooks/useQueries';
import { Skeleton } from '../components/Skeleton';

export const Stats = () => {
  const { t } = useTranslation();
  const { data: trendData, isLoading: trendLoading } = useStatsTrend();
  const { data: distData, isLoading: distLoading } = useStatsDistribution();

  const trend = trendData?.trends || [];
  const dist = distData?.distribution || [];
  const loading = trendLoading || distLoading;

  const COLORS = ['#00F2FF', '#39FF14', '#FF00FF', '#FFFF00', '#FF3131'];

  const tooltipStyle = {
    backgroundColor: '#121216',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '12px',
  };

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
        {/* Distance Trend Chart */}
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
            {loading ? <Skeleton className="h-full w-full" /> : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="colorDist" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00F2FF" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#00F2FF" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `${val.toFixed(1)}`} />
                  <Tooltip contentStyle={tooltipStyle} itemStyle={{ color: '#00F2FF' }} formatter={(value: number) => [`${value.toFixed(2)} km`, t('common.distance')]} />
                  <Area type="monotone" dataKey="distance_km" stroke="#00F2FF" strokeWidth={3} fillOpacity={1} fill="url(#colorDist)" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </motion.div>

        {/* Monthly Count Bar Chart */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.05 }}
          className="glass-card p-8 min-h-[400px]"
        >
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white tracking-tight uppercase">{t('stats.monthly_count')}</h3>
            <p className="text-slate-500 text-sm tracking-wide">{t('stats.monthly_count_sub')}</p>
          </div>
          <div className="h-64">
            {loading ? <Skeleton className="h-full w-full" /> : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trend}>
                  <defs>
                    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#39FF14" stopOpacity={0.8}/>
                      <stop offset="100%" stopColor="#39FF14" stopOpacity={0.2}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} allowDecimals={false} />
                  <Tooltip contentStyle={tooltipStyle} formatter={(value: number) => [value, t('stats.monthly_count')]} />
                  <Bar dataKey="count" fill="url(#barGrad)" radius={[6, 6, 0, 0]} maxBarSize={40} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </motion.div>

        {/* Distribution Donut Chart */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-8 min-h-[400px] lg:col-span-2"
        >
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white tracking-tight uppercase">{t('stats.activity_profile')}</h3>
            <p className="text-slate-500 text-sm tracking-wide">{t('stats.activity_sub')}</p>
          </div>
          <div className="h-64">
            {loading ? <Skeleton className="h-32 w-32 mx-auto rounded-full" /> : (
              <>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={dist} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={8} dataKey="count" nameKey="type">
                      {dist.map((_entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={tooltipStyle} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="flex flex-wrap justify-center gap-4 mt-4">
                  {dist.map((d: any, i: number) => (
                    <div key={d.type} className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                      <span className="text-xs font-bold text-slate-400 uppercase tracking-tighter">{d.type}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};
