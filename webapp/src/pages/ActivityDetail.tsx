import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Polyline, Marker, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import polylineLib from 'polyline';
import { activityService } from '../services/api';
import { useActivity, useDeleteActivity, useUpdateActivity } from '../hooks/useQueries';
import { useToast } from '../components/Toast';
import { DetailSkeleton } from '../components/Skeleton';
import { 
  ArrowLeft, Download, FileDown, Trash2, Pencil, Check, X,
  Heart, Footprints, Mountain, Flame, Clock, MapPin, Gauge, TrendingUp,
  StickyNote
} from 'lucide-react';

// Fix leaflet icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const FitBounds = ({ coords }: { coords: [number, number][] }) => {
  const map = useMap();
  useEffect(() => {
    if (coords.length > 0) {
      map.fitBounds(L.latLngBounds(coords), { padding: [40, 40] });
    }
  }, [coords, map]);
  return null;
};

const ACTIVITY_TYPE_MAP: Record<string, string> = {
  'Running': '跑步', 'Hiking': '徒步', 'Mountaineering': '登山',
  'Cycling': '骑行', 'Swimming': '游泳', 'Training': '训练',
  'Walking': '步行', 'Trail Running': '越野跑',
};

const ACTIVITY_TYPES = ['Running', 'Hiking', 'Cycling', 'Swimming', 'Mountaineering', 'Training', 'Walking', 'Trail Running'];

export const ActivityDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const toast = useToast();
  const isZh = i18n.language.startsWith('zh');

  const activityId = Number(id);
  const { data: activity, isLoading, isError } = useActivity(activityId);
  const deleteMutation = useDeleteActivity();
  const updateMutation = useUpdateActivity();

  const [coords, setCoords] = useState<[number, number][]>([]);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  // Edit states
  const [editing, setEditing] = useState(false);
  const [editType, setEditType] = useState('');
  const [editDistance, setEditDistance] = useState('');
  const [editNotes, setEditNotes] = useState('');

  useEffect(() => {
    if (activity?.polyline) {
      setCoords(polylineLib.decode(activity.polyline) as [number, number][]);
    }
    if (activity) {
      setEditType(activity.activity_type);
      setEditDistance((activity.distance_m / 1000).toFixed(2));
      setEditNotes(activity.notes || '');
    }
  }, [activity]);

  if (isError) {
    navigate('/explorer');
    return null;
  }
  if (isLoading || !activity) return <DetailSkeleton />;

  const handleDelete = async () => {
    try {
      await deleteMutation.mutateAsync(activity.id);
      toast.success(isZh ? '活动已删除' : 'Activity deleted');
      navigate('/explorer');
    } catch {
      toast.error(isZh ? '删除失败' : 'Delete failed');
    }
  };

  const handleSave = async () => {
    const distanceM = parseFloat(editDistance) * 1000;
    if (isNaN(distanceM)) {
      toast.error(isZh ? '距离输入无效' : 'Invalid distance');
      return;
    }

    try {
      await updateMutation.mutateAsync({ 
        id: activity.id, 
        data: { 
          activity_type: editType,
          distance_m: distanceM,
          notes: editNotes
        } 
      });
      toast.success(isZh ? '更新成功' : 'Updated successfully');
      setEditing(false);
    } catch {
      toast.error(isZh ? '更新失败' : 'Update failed');
    }
  };

  const getDisplayType = (type: string) => isZh && ACTIVITY_TYPE_MAP[type] ? ACTIVITY_TYPE_MAP[type] : type;

  const formatPace = (paceS?: number | null) => {
    if (!paceS) return '--';
    const mins = Math.floor(paceS / 60);
    const secs = Math.round(paceS % 60);
    return `${mins}'${secs.toString().padStart(2, '0')}"`;
  };

  const metrics = [
    { icon: MapPin, label: t('detail.distance', '距离'), value: `${(activity.distance_m / 1000).toFixed(2)}`, unit: t('common.km'), color: 'text-cyber-cyan' },
    { icon: Clock, label: t('detail.duration', '时长'), value: `${(activity.duration_s / 60).toFixed(0)}`, unit: t('common.min'), color: 'text-white' },
    { icon: Gauge, label: t('detail.pace', '配速'), value: formatPace((activity as any).avg_pace_s_per_km), unit: '/km', color: 'text-cyber-green' },
    { icon: Heart, label: t('detail.heart_rate', '心率'), value: activity.avg_heart_rate?.toFixed(0) || '--', unit: t('common.bpm'), color: 'text-red-400' },
    { icon: Footprints, label: t('detail.cadence', '步频'), value: activity.avg_cadence?.toFixed(0) || '--', unit: t('common.spm'), color: 'text-blue-400' },
    { icon: TrendingUp, label: t('detail.stride', '步幅'), value: activity.avg_stride_length_m?.toFixed(2) || '--', unit: t('common.m'), color: 'text-purple-400' },
    { icon: Mountain, label: t('detail.ascent', '爬升'), value: activity.total_ascent_m?.toFixed(0) || '--', unit: t('common.m'), color: 'text-emerald-400' },
    { icon: Flame, label: t('detail.calories', '卡路里'), value: activity.calories_kcal?.toFixed(0) || '--', unit: t('common.kcal'), color: 'text-orange-400' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors"
          >
            <ArrowLeft size={18} />
          </button>
          <div>
            {editing ? (
              <div className="flex items-center gap-2">
                <select
                  value={editType}
                  onChange={e => setEditType(e.target.value)}
                  className="bg-white/5 border border-white/10 rounded-xl px-3 py-1.5 text-white text-2xl font-black focus:outline-none focus:border-cyber-cyan"
                >
                  {ACTIVITY_TYPES.map(type => (
                    <option key={type} value={type} className="bg-obsidian">{getDisplayType(type)}</option>
                  ))}
                </select>
                <button onClick={handleSave} className="w-8 h-8 rounded-lg bg-cyber-green/20 flex items-center justify-center text-cyber-green hover:bg-cyber-green/30">
                  <Check size={16} />
                </button>
                <button onClick={() => { setEditing(false); setEditType(activity.activity_type); setEditDistance((activity.distance_m/1000).toFixed(2)); setEditNotes(activity.notes || ''); }} className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-slate-400 hover:bg-white/10">
                  <X size={16} />
                </button>
              </div>
            ) : (
              <motion.h1
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-3xl font-black text-white tracking-tighter flex items-center gap-3"
              >
                {getDisplayType(activity.activity_type)}
                <button onClick={() => setEditing(true)} className="w-7 h-7 rounded-lg bg-white/5 flex items-center justify-center text-slate-500 hover:text-cyber-cyan hover:bg-white/10 transition-colors">
                  <Pencil size={12} />
                </button>
              </motion.h1>
            )}
            <p className="text-slate-500 text-sm font-mono">
              {new Date(activity.start_time).toLocaleDateString()} • {activity.source_device}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <a href={activityService.getOriginalFileUrl(activity.id)} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyber-cyan/10 text-cyber-cyan text-sm font-bold hover:bg-cyber-cyan/20 transition-colors" download>
            <Download size={14} />
            {t('detail.download_original', '原始文件')}
          </a>
          <a href={activityService.getGpxExportUrl(activity.id)} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyber-green/10 text-cyber-green text-sm font-bold hover:bg-cyber-green/20 transition-colors" download>
            <FileDown size={14} />
            {t('detail.export_gpx', '导出 GPX')}
          </a>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-500/10 text-red-400 text-sm font-bold hover:bg-red-500/20 transition-colors"
          >
            <Trash2 size={14} />
            {t('detail.delete', '删除')}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {metrics.map((m, i) => (
              <motion.div
                key={m.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card p-5"
              >
                <div className="flex items-center gap-2 mb-2">
                  <m.icon size={14} className={m.color} />
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{m.label}</span>
                </div>
                {editing && m.label === t('detail.distance', '距离') ? (
                  <div className="flex items-baseline gap-1">
                    <input 
                      type="text" 
                      value={editDistance} 
                      onChange={e => setEditDistance(e.target.value)}
                      className="bg-white/5 border border-white/10 rounded px-2 py-0.5 text-2xl font-black text-white w-24 focus:outline-none focus:border-cyber-cyan"
                    />
                    <span className="text-xs font-bold text-cyber-cyan">{m.unit}</span>
                  </div>
                ) : (
                  <p className="text-2xl font-black text-white">
                    {m.value} <span className={`text-xs font-bold ${m.color}`}>{m.unit}</span>
                  </p>
                )}
              </motion.div>
            ))}
          </div>

          {/* Map */}
          {coords.length > 0 && (
            <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="glass-card overflow-hidden h-[400px]">
              <MapContainer center={coords[0]} zoom={14} className="h-full w-full" zoomControl={false}>
                <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; CARTO' />
                <Polyline positions={coords} pathOptions={{ color: '#00F2FF', weight: 4, opacity: 0.8 }} />
                <Marker position={coords[0]} />
                <Marker position={coords[coords.length - 1]} />
                <FitBounds coords={coords} />
              </MapContainer>
            </motion.div>
          )}
        </div>

        {/* Notes Sidebar */}
        <div className="space-y-6">
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-card p-6 h-full min-h-[300px] border-white/5 flex flex-col"
          >
            <div className="flex items-center gap-2 mb-4">
              <StickyNote size={18} className="text-cyber-green" />
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400">{isZh ? '备注' : 'Notes'}</h3>
            </div>
            {editing ? (
              <textarea
                value={editNotes}
                onChange={e => setEditNotes(e.target.value)}
                placeholder={isZh ? '记录下此刻的感受...' : 'Write something about this session...'}
                className="flex-1 bg-white/5 border border-white/10 rounded-xl p-4 text-slate-300 text-sm focus:outline-none focus:border-cyber-green resize-none"
              />
            ) : (
              <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap flex-1 italic">
                {activity.notes || (isZh ? '暂无备注' : 'No notes available')}
              </p>
            )}
            
            {!editing && (
              <button 
                onClick={() => setEditing(true)}
                className="mt-4 text-[10px] font-black uppercase text-cyber-green hover:underline flex items-center gap-1"
              >
                <Pencil size={10} />
                {isZh ? '修改备注' : 'Edit Notes'}
              </button>
            )}
          </motion.div>
        </div>
      </div>

      {/* Delete Confirm Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[9999]">
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="glass-card p-8 max-w-md w-full mx-4 border border-red-500/30">
            <h3 className="text-xl font-bold text-white mb-2">{t('detail.confirm_delete_title', '确认删除')}</h3>
            <p className="text-slate-400 mb-6">{t('detail.confirm_delete_msg', '此操作不可撤销，确定要删除这条运动记录吗？')}</p>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setShowDeleteConfirm(false)} className="px-6 py-2 rounded-xl bg-white/5 text-white text-sm font-bold hover:bg-white/10 transition-colors">
                {t('detail.cancel', '取消')}
              </button>
              <button onClick={handleDelete} disabled={deleteMutation.isPending} className="px-6 py-2 rounded-xl bg-red-500 text-white text-sm font-bold hover:bg-red-600 transition-colors disabled:opacity-50">
                {deleteMutation.isPending ? '...' : t('detail.confirm_delete', '确认删除')}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};
