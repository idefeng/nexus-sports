import { useEffect, useState } from 'react';
import { 
  Trophy, 
  MapPin, 
  Clock, 
  Flame, 
  ChevronRight,
  TrendingUp,
  Activity as ActivityIcon
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { MetricCard } from '../components/MetricCard';
import { activityService } from '../services/api';
import type { Activity, StatsSummary } from '../types';

export const Dashboard = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, activitiesData] = await Promise.all([
          activityService.getStatsSummary(),
          activityService.getActivities()
        ]);
        setStats(statsData);
        setActivities(activitiesData.slice(0, 5)); // Just recent ones
      } catch (error) {
        console.error('Failed to fetch dashboard data', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-cyber-cyan"></div>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <header>
        <motion.h1 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-4xl font-black text-white tracking-tighter"
        >
          {t('common.athlete_performance')} <span className="text-cyber-cyan italic">{t('common.hub')}</span>
        </motion.h1>
        <p className="text-slate-500 font-medium mt-1 tracking-wider uppercase">{t('common.sub_header')}</p>
      </header>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          label={t('common.total_sessions')} 
          value={stats?.total_activities || 0} 
          icon={ActivityIcon} 
          color="white"
        />
        <MetricCard 
          label={t('common.cumulative_distance')} 
          value={`${stats?.total_distance_km.toFixed(1) || 0} ${t('common.km')}`} 
          icon={MapPin} 
          color="cyan"
        />
        <MetricCard 
          label={t('common.training_time')} 
          value={`${stats?.total_duration_hours.toFixed(1) || 0} ${t('common.h')}`} 
          icon={Clock} 
          color="green"
        />
        <MetricCard 
          label={t('common.active_calories')} 
          value={`${stats?.total_calories_kcal.toFixed(0) || 0} ${t('common.kcal')}`} 
          icon={Flame} 
          color="magenta"
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activities */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <TrendingUp className="text-cyber-cyan" size={20} />
              {t('common.recent_activities')}
            </h2>
            <button className="text-sm font-bold text-cyber-cyan hover:underline">{t('common.view_all')}</button>
          </div>

          <div className="space-y-4">
            {activities.map((activity, idx) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="glass-card p-5 flex items-center justify-between group hover:border-cyber-cyan/30 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-5">
                  <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center group-hover:bg-cyber-cyan group-hover:text-black transition-colors">
                    <Trophy size={20} />
                  </div>
                  <div>
                    <h4 className="font-bold text-lg leading-tight">{activity.activity_type}</h4>
                    <p className="text-slate-500 text-sm font-medium">
                      {new Date(activity.start_time).toLocaleDateString()} • {activity.source_device}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-12">
                  <div className="text-right">
                    <p className="text-xs font-bold text-slate-500 uppercase">{t('common.distance')}</p>
                    <p className="text-lg font-black text-white italic">{(activity.distance_m/1000).toFixed(2)} {t('common.km')}</p>
                  </div>
                  <div className="text-right hidden sm:block">
                    <p className="text-xs font-bold text-slate-500 uppercase">{t('common.duration')}</p>
                    <p className="text-lg font-bold text-white">{(activity.duration_s/60).toFixed(0)} {t('common.min')}</p>
                  </div>
                  <ChevronRight size={20} className="text-slate-600 group-hover:text-cyber-cyan transition-colors" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* AI Insight Placeholder */}
        <div className="space-y-6">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <ActivityIcon className="text-cyber-green" size={20} />
            {t('common.ai_analysis')}
          </h2>
          <div className="glass-card p-6 border-cyber-green/20 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-cyber-green/10 blur-3xl rounded-full" />
            <p className="text-cyber-green font-mono text-xs mb-4">MATCHING AGENT INPUT...</p>
            <p className="text-slate-300 font-medium leading-relaxed">
              "Based on your last 3 mountain climbing sessions, your anaerobic capacity has increased by 4.2%. Recovery time suggested: 18 hours."
            </p>
            <button className="mt-6 w-full py-3 rounded-xl border border-cyber-green/30 text-cyber-green text-sm font-bold uppercase tracking-widest hover:bg-cyber-green hover:text-black transition-all">
              Detailed Rapport
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
