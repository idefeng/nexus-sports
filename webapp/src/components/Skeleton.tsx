import { motion } from 'framer-motion';

/** Pulsating skeleton bar used as placeholder during data loading. */
export const Skeleton = ({ className = '' }: { className?: string }) => (
  <motion.div
    className={`bg-white/5 rounded-xl ${className}`}
    animate={{ opacity: [0.3, 0.6, 0.3] }}
    transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
  />
);

/** Dashboard skeleton: 4 metric cards + 3 activity rows */
export const DashboardSkeleton = () => (
  <div className="space-y-10 animate-pulse">
    <div>
      <Skeleton className="h-10 w-80 mb-2" />
      <Skeleton className="h-4 w-48" />
    </div>
    <div className="grid grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <Skeleton key={i} className="h-28" />
      ))}
    </div>
    <div className="grid grid-cols-3 gap-8">
      <div className="col-span-2 space-y-4">
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} className="h-20" />
        ))}
      </div>
      <Skeleton className="h-60" />
    </div>
  </div>
);

/** Activity detail skeleton: header + metrics + map */
export const DetailSkeleton = () => (
  <div className="space-y-8 animate-pulse">
    <div className="flex items-center gap-4">
      <Skeleton className="h-10 w-10 rounded-full" />
      <div>
        <Skeleton className="h-8 w-32 mb-2" />
        <Skeleton className="h-4 w-48" />
      </div>
    </div>
    <div className="grid grid-cols-4 gap-4">
      {[...Array(8)].map((_, i) => (
        <Skeleton key={i} className="h-24" />
      ))}
    </div>
    <Skeleton className="h-[400px]" />
  </div>
);
