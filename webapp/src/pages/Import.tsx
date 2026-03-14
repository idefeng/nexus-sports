import { useState, useCallback } from 'react';
import { Upload, File, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { useUploadFiles } from '../hooks/useQueries';
import { useToast } from '../components/Toast';

interface UploadResult {
  filename: string;
  status: 'success' | 'failed' | 'skipped';
  message: string;
  activities?: {
    type: string;
    start_time: string;
    distance_m: number;
  }[];
}

export const Import = () => {
  const { t, i18n } = useTranslation();
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<UploadResult[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const isZh = i18n.language.startsWith('zh');

  const toast = useToast();
  const uploadMutation = useUploadFiles();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      f => f.name.endsWith('.fit') || f.name.endsWith('.gpx') || f.name.endsWith('.zip')
    );
    if (droppedFiles.length > 0) setFiles(droppedFiles);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleUpload = async () => {
    if (files.length === 0) return;
    setResults([]);
    try {
      const data = await uploadMutation.mutateAsync(files);
      setResults(data.results || []);
      setFiles([]);
      toast.success(isZh ? '处理完成' : 'Processing complete');
    } catch (error: any) {
      console.error('Upload failed', error);
      toast.error(isZh ? `上传失败: ${error.message}` : `Upload failed: ${error.message}`);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-10">
      <header className="text-center">
        <motion.div 
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-20 h-20 bg-cyber-cyan/10 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-[0_0_30px_rgba(0,242,255,0.2)] border border-cyber-cyan/20"
        >
          <Upload className="text-cyber-cyan" size={32} />
        </motion.div>
        <h1 className="text-4xl font-black text-white tracking-tight leading-tight uppercase tracking-tighter">
          {t('import.header')} <span className="text-cyber-cyan italic">{t('import.assets')}</span>
        </h1>
        <p className="text-slate-500 font-medium mt-2 uppercase tracking-widest text-sm italic">{t('import.sub')}</p>
      </header>

      <div 
        className={`glass-card p-10 border-dashed border-2 transition-all text-center group ${
          isDragging 
            ? 'border-cyber-cyan bg-cyber-cyan/5 scale-[1.02]' 
            : 'border-white/5 hover:border-cyber-cyan/30'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <input 
          type="file" 
          id="file-upload" 
          multiple 
          accept=".zip,.fit,.gpx" 
          className="hidden" 
          onChange={handleFileChange}
        />
        <label htmlFor="file-upload" className="cursor-pointer block">
          <File className={`mx-auto mb-4 transition-all ${
            isDragging ? 'text-cyber-cyan scale-125' : 'text-slate-600 group-hover:text-cyber-cyan group-hover:scale-110'
          }`} size={48} />
          <p className="text-lg font-bold text-white mb-1 uppercase tracking-tight">{t('import.select_files')}</p>
          <p className="text-slate-500 text-sm italic">{t('import.drag_drop')}</p>
        </label>

        {files.length > 0 && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            className="mt-8 pt-8 border-t border-white/5 space-y-2"
          >
            {files.map(f => (
              <div key={f.name} className="flex items-center gap-2 text-xs font-mono text-cyber-cyan bg-cyber-cyan/5 px-3 py-2 rounded-lg">
                <File size={14} />
                {f.name}
                <span className="ml-auto text-slate-500">{(f.size / 1024).toFixed(0)} KB</span>
              </div>
            ))}
            <button 
              onClick={handleUpload}
              disabled={uploadMutation.isPending}
              className="mt-6 cyber-button w-full flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {uploadMutation.isPending ? <Loader2 className="animate-spin" size={20} /> : <Upload size={20} />}
              {uploadMutation.isPending ? t('import.processing') : t('import.initialize')}
            </button>
          </motion.div>
        )}
      </div>

      <AnimatePresence>
        {results.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-3"
          >
            <h3 className="text-sm font-black text-slate-500 tracking-widest uppercase mb-4">{t('import.results')}</h3>
            {results.map((res, i) => (
              <div key={i} className={`glass-card p-4 flex items-center justify-between border-l-4 ${
                res.status === 'success' ? 'border-l-cyber-green' : res.status === 'skipped' ? 'border-l-yellow-500' : 'border-l-red-500'
              }`}>
                <div className="flex items-center gap-3">
                  {res.status === 'success' ? (
                    <CheckCircle2 className="text-cyber-green" size={18} />
                  ) : res.status === 'skipped' ? (
                    <AlertCircle className="text-yellow-500" size={18} />
                  ) : (
                    <AlertCircle className="text-red-500" size={18} />
                  )}
                  <div>
                    <p className="text-sm font-bold text-white">{res.filename}</p>
                    <p className="text-xs text-slate-500 uppercase">{res.message}</p>
                    
                    {res.activities && res.activities.length > 0 && (
                      <div className="mt-3 space-y-1 border-t border-white/5 pt-2">
                        {res.activities.slice(0, 3).map((act, j) => (
                          <div key={j} className="flex items-center gap-2 text-[10px] text-slate-400 font-mono">
                            <span className="text-cyber-cyan">{act.type}</span>
                            <span>•</span>
                            <span>{new Date(act.start_time).toLocaleDateString()}</span>
                            <span>•</span>
                            <span>{(act.distance_m / 1000).toFixed(2)} km</span>
                          </div>
                        ))}
                        {res.activities.length > 3 && (
                          <p className="text-[10px] text-slate-500 italic">...and {res.activities.length - 3} more</p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
