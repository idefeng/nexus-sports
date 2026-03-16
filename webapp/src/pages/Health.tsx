import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Plus, Trash2, Activity } from 'lucide-react';
import api from '../lib/axios';

interface BodyMetrics {
  id: number;
  recorded_at: string;
  height_cm: number | null;
  weight_kg: number | null;
  bust_cm: number | null;
  waist_cm: number | null;
  hips_cm: number | null;
}

export const Health = () => {
  const { t } = useTranslation();
  const [metrics, setMetrics] = useState<BodyMetrics[]>([]);
  const [latest, setLatest] = useState<BodyMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    recorded_at: new Date().toISOString().split('T')[0],
    height_cm: '',
    weight_kg: '',
    bust_cm: '',
    waist_cm: '',
    hips_cm: ''
  });

  const fetchData = async () => {
    try {
      const [metricsRes, latestRes] = await Promise.all([
        api.get('/metrics/'),
        api.get('/metrics/latest').catch(() => ({ data: null }))
      ]);
      setMetrics(metricsRes.data);
      setLatest(latestRes.data);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const dataToSend = {
        recorded_at: new Date(formData.recorded_at).toISOString(),
        height_cm: formData.height_cm ? parseFloat(formData.height_cm) : null,
        weight_kg: formData.weight_kg ? parseFloat(formData.weight_kg) : null,
        bust_cm: formData.bust_cm ? parseFloat(formData.bust_cm) : null,
        waist_cm: formData.waist_cm ? parseFloat(formData.waist_cm) : null,
        hips_cm: formData.hips_cm ? parseFloat(formData.hips_cm) : null,
      };
      await api.post('/metrics/', dataToSend);
      setShowForm(false);
      setFormData({
        recorded_at: new Date().toISOString().split('T')[0],
        height_cm: '',
        weight_kg: '',
        bust_cm: '',
        waist_cm: '',
        hips_cm: ''
      });
      fetchData();
    } catch (error) {
      console.error('Error adding metrics:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm(t('detail.confirm_delete_msg'))) return;
    try {
      await api.delete(`/metrics/${id}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting metrics:', error);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-500">Loading...</div>;

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <motion.h1 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-4xl font-black text-white tracking-tighter"
          >
            {t('common.health')} <span className="text-cyber-green italic">INSIGHTS</span>
          </motion.h1>
          <p className="text-slate-500 font-medium mt-1 tracking-wider uppercase">Record and track your body evolution</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="bg-cyber-green text-black px-6 py-2 rounded-xl font-bold flex items-center gap-2 hover:shadow-[0_0_20px_rgba(0,255,157,0.4)] transition-all"
        >
          <Plus size={20} />
          {t('common.add_record')}
        </button>
      </header>

      {showForm && (
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-8 border-cyber-green/20"
        >
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.recorded_at')}</label>
              <input 
                type="date" 
                value={formData.recorded_at}
                onChange={(e) => setFormData({...formData, recorded_at: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.height')} (cm)</label>
              <input 
                type="number" step="0.1"
                placeholder="175.0"
                value={formData.height_cm}
                onChange={(e) => setFormData({...formData, height_cm: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.weight')} (kg)</label>
              <input 
                type="number" step="0.1"
                placeholder="70.0"
                value={formData.weight_kg}
                onChange={(e) => setFormData({...formData, weight_kg: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.bust')} (cm)</label>
              <input 
                type="number" step="0.1"
                value={formData.bust_cm}
                onChange={(e) => setFormData({...formData, bust_cm: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.waist')} (cm)</label>
              <input 
                type="number" step="0.1"
                value={formData.waist_cm}
                onChange={(e) => setFormData({...formData, waist_cm: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">{t('common.hips')} (cm)</label>
              <input 
                type="number" step="0.1"
                value={formData.hips_cm}
                onChange={(e) => setFormData({...formData, hips_cm: e.target.value})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cyber-green outline-none"
              />
            </div>
            <div className="md:col-span-3 flex justify-end gap-4 mt-4">
              <button 
                type="button" 
                onClick={() => setShowForm(false)}
                className="text-slate-400 font-bold hover:text-white transition-colors"
              >
                {t('detail.cancel')}
              </button>
              <button 
                type="submit"
                className="bg-cyber-green text-black px-8 py-2 rounded-xl font-bold"
              >
                {t('common.confirm_delete').replace(t('detail.delete'), t('common.add_record'))}
              </button>
            </div>
          </form>
        </motion.div>
      )}

      {/* Latest Stats */}
      {latest && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <div className="glass-card p-6 border-cyber-green/10">
            <p className="text-xs font-bold text-slate-500 mb-1 uppercase tracking-widest">{t('common.weight')}</p>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-black text-white italic">{latest.weight_kg}</span>
              <span className="text-sm font-bold text-slate-500 mb-1">KG</span>
            </div>
          </div>
          <div className="glass-card p-6 border-cyber-green/10">
            <p className="text-xs font-bold text-slate-500 mb-1 uppercase tracking-widest">{t('common.height')}</p>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-black text-white italic">{latest.height_cm}</span>
              <span className="text-sm font-bold text-slate-500 mb-1">CM</span>
            </div>
          </div>
          <div className="glass-card p-6 border-cyber-green/10">
            <p className="text-xs font-bold text-slate-500 mb-1 uppercase tracking-widest">{t('common.bust')}</p>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-black text-white italic">{latest.bust_cm || '-'}</span>
              <span className="text-sm font-bold text-slate-500 mb-1">CM</span>
            </div>
          </div>
          <div className="glass-card p-6 border-cyber-green/10">
            <p className="text-xs font-bold text-slate-500 mb-1 uppercase tracking-widest">{t('common.waist')}</p>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-black text-white italic">{latest.waist_cm || '-'}</span>
              <span className="text-sm font-bold text-slate-500 mb-1">CM</span>
            </div>
          </div>
          <div className="glass-card p-6 border-cyber-green/10">
            <p className="text-xs font-bold text-slate-500 mb-1 uppercase tracking-widest">{t('common.hips')}</p>
            <div className="flex items-end gap-2">
              <span className="text-3xl font-black text-white italic">{latest.hips_cm || '-'}</span>
              <span className="text-sm font-bold text-slate-500 mb-1">CM</span>
            </div>
          </div>
        </div>
      )}

      {/* History Table */}
      <div className="glass-card overflow-hidden">
        <div className="p-6 border-b border-white/5 flex items-center gap-2">
          <Activity className="text-cyber-green" size={20} />
          <h2 className="text-xl font-bold">{t('common.history')}</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-white/5 text-slate-500 text-xs font-bold uppercase tracking-widest">
                <th className="px-6 py-4">{t('common.recorded_at')}</th>
                <th className="px-6 py-4">{t('common.weight')}</th>
                <th className="px-6 py-4">{t('common.height')}</th>
                <th className="px-6 py-4">{t('common.bust')}</th>
                <th className="px-6 py-4">{t('common.waist')}</th>
                <th className="px-6 py-4">{t('common.hips')}</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {metrics.map((m) => (
                <tr key={m.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 font-medium text-slate-300">
                    {new Date(m.recorded_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 font-black text-white italic">{m.weight_kg} kg</td>
                  <td className="px-6 py-4 text-slate-300">{m.height_cm} cm</td>
                  <td className="px-6 py-4 text-slate-300">{m.bust_cm || '-'}</td>
                  <td className="px-6 py-4 text-slate-300">{m.waist_cm || '-'}</td>
                  <td className="px-6 py-4 text-slate-300">{m.hips_cm || '-'}</td>
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => handleDelete(m.id)}
                      className="text-slate-600 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
