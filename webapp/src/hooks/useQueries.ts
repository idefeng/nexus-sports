/**
 * React Query hooks for Nexus Sports data fetching.
 * Replaces manual useEffect + useState patterns with cached, reactive queries.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { activityService } from '../services/api';

// ── Query Keys ──────────────────────────────────────────────
export const queryKeys = {
  activities: (skip?: number, limit?: number) => ['activities', { skip, limit }] as const,
  activity: (id: number) => ['activity', id] as const,
  statsSummary: ['stats', 'summary'] as const,
  statsTrend: ['stats', 'trend'] as const,
  statsDistribution: ['stats', 'distribution'] as const,
  aiLatest: ['ai', 'latest'] as const,
  aiMonthly: (month?: string) => ['ai', 'monthly', month] as const,
};

// ── Queries ─────────────────────────────────────────────────
export const useActivities = (skip = 0, limit = 200) =>
  useQuery({
    queryKey: queryKeys.activities(skip, limit),
    queryFn: () => activityService.getActivities(skip, limit),
  });

export const useActivity = (id: number) =>
  useQuery({
    queryKey: queryKeys.activity(id),
    queryFn: () => activityService.getActivity(id),
    enabled: id > 0,
  });

export const useStatsSummary = () =>
  useQuery({
    queryKey: queryKeys.statsSummary,
    queryFn: () => activityService.getStatsSummary(),
  });

export const useStatsTrend = () =>
  useQuery({
    queryKey: queryKeys.statsTrend,
    queryFn: () => activityService.getStatsTrend(),
  });

export const useStatsDistribution = () =>
  useQuery({
    queryKey: queryKeys.statsDistribution,
    queryFn: () => activityService.getStatsDistribution(),
  });

export const useLatestAIReport = () =>
  useQuery({
    queryKey: queryKeys.aiLatest,
    queryFn: () => activityService.getLatestAIReport(),
    retry: false,
  });

// ── Mutations ───────────────────────────────────────────────
export const useDeleteActivity = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => activityService.deleteActivity(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activities'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
  });
};

export const useUpdateActivity = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Record<string, any> }) =>
      activityService.updateActivity(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.activity(variables.id) });
      queryClient.invalidateQueries({ queryKey: ['activities'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
  });
};

export const useUploadFiles = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (files: File[]) => activityService.uploadFiles(files),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activities'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['ai'] });
    },
  });
};
