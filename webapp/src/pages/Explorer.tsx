import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Polyline, Marker, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import polyline from 'polyline';
import { activityService } from '../services/api';
import { useActivities } from '../hooks/useQueries';
import type { Activity } from '../types';
import { Map as MapIcon, Download, FileDown, CheckSquare, Square, X, Loader2 } from 'lucide-react';
import { Skeleton } from '../components/Skeleton';
import { useToast } from '../components/Toast';

// Fix for default marker icons in Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const ChangeView = ({ center, bounds }: { center: L.LatLngExpression, bounds?: L.LatLngBoundsExpression }) => {
  const map = useMap();
  useEffect(() => {
    if (bounds) { map.fitBounds(bounds, { padding: [50, 50] }); }
    else { map.setView(center); }
  }, [center, bounds, map]);
  return null;
};

const ACTIVITY_TYPE_MAP: Record<string, string> = {
  'Running': '跑步', 'Hiking': '徒步', 'Mountaineering': '登山',
  'Cycling': '骑行', 'Swimming': '游泳', 'Training': '训练',
  'Walking': '步行', 'Trail Running': '越野跑',
};

export const Explorer = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const toast = useToast();
  const isZh = i18n.language.startsWith('zh');

  const { data: activitiesData, isLoading } = useActivities(0, 200);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [coords, setCoords] = useState<[number, number][]>([]);
  
  // Selection logic for batch export
  const [selectMode, setSelectMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [isExporting, setIsExporting] = useState(false);

  const activities = (activitiesData?.items || []).filter((a: Activity) => a.polyline);

  useEffect(() => {
    if (activities.length > 0 && !selectedActivity) {
      handleSelect(activities[0]);
    }
  }, [activities, selectedActivity]);

  const handleSelect = (act: Activity) => {
    if (selectMode) {
      toggleSelection(act.id);
      return;
    }
    setSelectedActivity(act);
    if (act.polyline) {
      const decoded = polyline.decode(act.polyline);
      setCoords(decoded as [number, number][]);
    }
  };

  const toggleSelection = (id: number) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };

  const handleBatchExport = async () => {
    if (selectedIds.length === 0) return;
    setIsExporting(true);
    try {
      await activityService.batchExport(selectedIds);
      toast.success(isZh ? '批量导出成功' : 'Batch export success');
      setSelectMode(false);
      setSelectedIds([]);
    } catch (e) {
      toast.error(isZh ? '导出失败' : 'Export failed');
    } finally {
      setIsExporting(false);
    }
  };

  const getDisplayType = (type: string) => isZh && ACTIVITY_TYPE_MAP[type] ? ACTIVITY_TYPE_MAP[type] : type;

  const center: L.LatLngExpression = coords.length > 0 ? coords[0] : [35.6895, 139.6917];
  const bounds = coords.length > 0 ? L.latLngBounds(coords) : undefined;

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      {/* Activity List Side */}
      <div className="w-80 flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <MapIcon className="text-cyber-cyan" size={20} />
            {t('explorer.header')}
          </h2>
          <button 
            onClick={() => { setSelectMode(!selectMode); setSelectedIds([]); }}
            className={`p-1.5 rounded-lg transition-colors ${selectMode ? 'bg-cyber-cyan text-black' : 'text-slate-500 hover:bg-white/5'}`}
          >
            {selectMode ? <X size={18} /> : <CheckSquare size={18} />}
          </button>
        </div>

        {selectMode && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="bg-cyber-cyan/10 p-3 rounded-xl border border-cyber-cyan/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-cyber-cyan">{selectedIds.length} {isZh ? '个已选择' : 'Selected'}</span>
              <button 
                disabled={selectedIds.length === 0 || isExporting}
                onClick={handleBatchExport}
                className="text-[10px] font-black uppercase bg-cyber-cyan text-black px-2 py-1 rounded hover:scale-105 disabled:opacity-50 transition-all flex items-center gap-1"
              >
                {isExporting ? <Loader2 size={10} className="animate-spin" /> : <Download size={10} />}
                {isZh ? '下载 ZIP' : 'Download ZIP'}
              </button>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setSelectedIds(activities.map((a: Activity) => a.id))} className="text-[9px] text-slate-400 hover:text-white uppercase font-bold">{isZh ? '全选' : 'Select All'}</button>
              <button onClick={() => setSelectedIds([])} className="text-[9px] text-slate-400 hover:text-white uppercase font-bold">{isZh ? '清空' : 'Clear'}</button>
            </div>
          </motion.div>
        )}

        <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
          {isLoading ? (
            [...Array(6)].map((_, i) => <Skeleton key={i} className="h-24 w-full" />)
          ) : (
            activities.map((act: Activity) => (
              <div 
                key={act.id}
                onClick={() => handleSelect(act)}
                onDoubleClick={() => !selectMode && navigate(`/activity/${act.id}`)}
                className={`
                  glass-card p-4 cursor-pointer border transition-all relative group
                  ${selectedActivity?.id === act.id && !selectMode ? 'border-cyber-cyan bg-cyber-cyan/5' : 'border-white/5 hover:border-white/20'}
                  ${selectedIds.includes(act.id) ? 'border-cyber-cyan/50 bg-cyber-cyan/5' : ''}
                `}
              >
                {selectMode && (
                  <div className="absolute top-4 right-4 text-cyber-cyan">
                    {selectedIds.includes(act.id) ? <CheckSquare size={16} /> : <Square size={16} className="text-slate-700" />}
                  </div>
                )}
                <div className="flex justify-between items-start mb-2">
                  <span className="text-[10px] font-black uppercase text-cyber-cyan tracking-widest">{getDisplayType(act.activity_type)}</span>
                  <span className="text-[10px] text-slate-500 font-mono">{new Date(act.start_time).toLocaleDateString()}</span>
                </div>
                <p className="font-bold text-sm truncate pr-6">{act.source_device || 'Unknown Device'}</p>
                <div className="flex justify-between mt-3 text-xs font-mono text-slate-400">
                  <span>{(act.distance_m/1000).toFixed(2)}{t('common.km')}</span>
                  <span>{(act.duration_s/60).toFixed(0)}{t('common.min')}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Map View */}
      <div className="flex-1 glass-card overflow-hidden relative">
        <MapContainer center={center} zoom={13} className="h-full w-full" zoomControl={false}>
          <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; CARTO' />
          <AnimatePresence>
            {coords.length > 0 && (
              <>
                <Polyline positions={coords} pathOptions={{ color: '#00F2FF', weight: 4, opacity: 0.8 }} />
                <Marker position={coords[0]} />
                <Marker position={coords[coords.length - 1]} />
                <ChangeView center={center} bounds={bounds} />
              </>
            )}
          </AnimatePresence>
        </MapContainer>

        {/* Floating Detail Overlay */}
        {selectedActivity && !selectMode && (
          <motion.div initial={{ y: 100, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="absolute bottom-6 left-6 right-6 glass-card p-6 bg-obsidian-light/90 z-[1000] border-t-cyber-cyan/30">
            <div className="grid grid-cols-5 gap-8">
              <div>
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">{t('explorer.heart_rate')}</p>
                <p className="text-xl font-black text-white">{selectedActivity.avg_heart_rate?.toFixed(0) || '--'} <span className="text-xs text-cyber-cyan">{t('common.bpm')}</span></p>
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">{t('explorer.cadence')}</p>
                <p className="text-xl font-black text-white">{selectedActivity.avg_cadence?.toFixed(0) || '--'} <span className="text-xs text-cyber-cyan">{t('common.spm')}</span></p>
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">{t('explorer.climb')}</p>
                <p className="text-xl font-black text-white">{selectedActivity.total_ascent_m?.toFixed(0) || '--'} <span className="text-xs text-cyber-cyan">{t('common.m')}</span></p>
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">{t('explorer.training_load')}</p>
                <p className="text-xl font-black text-white">{selectedActivity.training_load?.toFixed(1) || '--'}</p>
              </div>
              <div className="flex flex-col gap-2">
                <a href={activityService.getOriginalFileUrl(selectedActivity.id)} className="flex items-center gap-1.5 text-xs font-bold text-cyber-cyan bg-cyber-cyan/10 px-3 py-1.5 rounded-lg hover:bg-cyber-cyan/20 transition-colors" download>
                  <Download size={12} />
                  {t('explorer.download_original', 'Original')}
                </a>
                <a href={activityService.getGpxExportUrl(selectedActivity.id)} className="flex items-center gap-1.5 text-xs font-bold text-cyber-green bg-cyber-green/10 px-3 py-1.5 rounded-lg hover:bg-cyber-green/20 transition-colors" download>
                  <FileDown size={12} />
                  {t('explorer.export_gpx', 'GPX')}
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};
