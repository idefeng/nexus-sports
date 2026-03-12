import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import polyline from 'polyline';
import { activityService } from '../services/api';
import type { Activity } from '../types';
import { Map as MapIcon } from 'lucide-react';

// Fix for default marker icons in Leaflet + Spark
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const ChangeView = ({ center, bounds }: { center: L.LatLngExpression, bounds?: L.LatLngBoundsExpression }) => {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [50, 50] });
    } else {
      map.setView(center);
    }
  }, [center, bounds, map]);
  return null;
};

export const Explorer = () => {
  const { t } = useTranslation();
  const [activities, setActivities] = useState<Activity[]>([]);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [coords, setCoords] = useState<[number, number][]>([]);

  useEffect(() => {
    activityService.getActivities().then(data => {
      const withPoly = data.filter((a: Activity) => a.polyline);
      setActivities(withPoly);
      if (withPoly.length > 0) handleSelect(withPoly[0]);
    });
  }, []);

  const handleSelect = (act: Activity) => {
    setSelectedActivity(act);
    if (act.polyline) {
      const decoded = polyline.decode(act.polyline);
      setCoords(decoded as [number, number][]);
    }
  };

  const center: L.LatLngExpression = coords.length > 0 ? coords[0] : [35.6895, 139.6917]; // Tokyo default
  const bounds = coords.length > 0 ? L.latLngBounds(coords) : undefined;

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      {/* Activity List Side */}
      <div className="w-80 flex flex-col gap-4">
        <h2 className="text-xl font-bold flex items-center gap-2 mb-2">
          <MapIcon className="text-cyber-cyan" size={20} />
          {t('explorer.header')}
        </h2>
        <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
          {activities.map(act => (
            <div 
              key={act.id}
              onClick={() => handleSelect(act)}
              className={`
                glass-card p-4 cursor-pointer border transition-all
                ${selectedActivity?.id === act.id ? 'border-cyber-cyan bg-cyber-cyan/5' : 'border-white/5 hover:border-white/20'}
              `}
            >
              <div className="flex justify-between items-start mb-2">
                <span className="text-[10px] font-black uppercase text-cyber-cyan tracking-widest">{act.activity_type}</span>
                <span className="text-[10px] text-slate-500 font-mono">{new Date(act.start_time).toLocaleDateString()}</span>
              </div>
              <p className="font-bold text-sm truncate">{act.source_device || 'Unknown Device'}</p>
              <div className="flex justify-between mt-3 text-xs font-mono text-slate-400">
                <span>{(act.distance_m/1000).toFixed(2)}{t('common.km')}</span>
                <span>{(act.duration_s/60).toFixed(0)}{t('common.min')}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Map View */}
      <div className="flex-1 glass-card overflow-hidden relative">
        <MapContainer 
          center={center} 
          zoom={13} 
          className="h-full w-full"
          zoomControl={false}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; CARTO'
          />
          <AnimatePresence>
            {coords.length > 0 && (
              <>
                <Polyline 
                  positions={coords} 
                  pathOptions={{ color: '#00F2FF', weight: 4, opacity: 0.8 }} 
                />
                <Marker position={coords[0]} />
                <Marker position={coords[coords.length - 1]} />
                <ChangeView center={center} bounds={bounds} />
              </>
            )}
          </AnimatePresence>
        </MapContainer>

        {/* Floating Detail Overlay */}
        {selectedActivity && (
          <motion.div 
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="absolute bottom-6 left-6 right-6 glass-card p-6 bg-obsidian-light/90 z-[1000] border-t-cyber-cyan/30"
          >
            <div className="grid grid-cols-4 gap-8">
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
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};
