import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  en: {
    translation: {
      common: {
        dashboard: 'Dashboard',
        statistics: 'Statistics',
        explorer: 'Explorer',
        import: 'Import',
        settings: 'Settings',
        health: 'Health Metrics',
        total_sessions: 'Total Sessions',
        cumulative_distance: 'Cumulative Distance',
        training_time: 'Training Time',
        active_calories: 'Active Calories',
        recent_activities: 'Recent Activities',
        view_all: 'View All',
        ai_analysis: 'AI Analysis',
        ai_no_data: 'No recent activity data available for AI analysis.',
        athlete_performance: 'Athlete Performance',
        hub: 'Hub',
        sub_header: 'Real-time multi-source activity aggregator',
        distance: 'Distance',
        duration: 'Duration',
        bpm: 'bpm',
        spm: 'spm',
        m: 'm',
        min: 'min',
        km: 'km',
        h: 'h',
        kcal: 'kcal',
        weight: 'Weight',
        height: 'Height',
        bust: 'Bust',
        waist: 'Waist',
        hips: 'Hips',
        recorded_at: 'Date',
        add_record: 'Add Record',
        history: 'History',
        latest: 'Latest Indicators'
      },
      stats: {
        header: 'Analytics',
        insights: 'Insights',
        sub: 'Advanced data visualization & trend analysis',
        monthly_progression: 'Monthly Progression',
        monthly_sub: 'Distance accumulated per month (km)',
        monthly_count: 'Monthly Sessions',
        monthly_count_sub: 'Number of activities per month',
        activity_profile: 'Activity Profile',
        activity_sub: 'Distribution by exercise type'
      },
      explorer: {
        header: 'Explorer',
        moving: 'Moving',
        heart_rate: 'Heart Rate',
        cadence: 'Cadence',
        climb: 'Climb',
        training_load: 'Training Load',
        download_original: 'Original',
        export_gpx: 'GPX'
      },
      import: {
        header: 'Ingest',
        assets: 'Assets',
        sub: 'Synchronize your multi-brand sports data',
        select_files: 'Select FIT, GPX or ZIP files',
        drag_drop: 'Drag and drop or click to browse',
        initialize: 'Initialize Upload',
        processing: 'Processing...',
        results: 'Ingestion Results'
      },
      detail: {
        distance: 'Distance',
        duration: 'Duration',
        pace: 'Pace',
        heart_rate: 'Heart Rate',
        cadence: 'Cadence',
        stride: 'Stride',
        ascent: 'Ascent',
        calories: 'Calories',
        download_original: 'Original File',
        export_gpx: 'Export GPX',
        delete: 'Delete',
        confirm_delete_title: 'Confirm Delete',
        confirm_delete_msg: 'This action cannot be undone. Are you sure you want to delete this activity?',
        cancel: 'Cancel',
        confirm_delete: 'Delete'
      }
    }
  },
  zh: {
    translation: {
      common: {
        dashboard: '看板',
        statistics: '数据统计',
        explorer: '运动浏览器',
        import: '导入数据',
        settings: '设置',
        health: '健康数据',
        total_sessions: '总运动次数',
        cumulative_distance: '累计距离',
        training_time: '累计时长',
        active_calories: '活动消耗',
        recent_activities: '最近运动记录',
        view_all: '查看全部',
        ai_analysis: 'AI 深度分析',
        ai_no_data: '暂无运动数据可供 AI 分析。',
        athlete_performance: '运动员性能',
        hub: '中心',
        sub_header: '实时多源运动数据聚合器',
        distance: '距离',
        duration: '时长',
        bpm: '次/分',
        spm: '步/分',
        m: '米',
        min: '分钟',
        km: '公里',
        h: '小时',
        kcal: '千卡',
        weight: '体重',
        height: '身高',
        bust: '胸围',
        waist: '腰围',
        hips: '臀围',
        recorded_at: '记录日期',
        add_record: '新增记录',
        history: '历史记录',
        latest: '最新指标'
      },
      stats: {
        header: '分析',
        insights: '洞察',
        sub: '进阶数据可视化与趋势分析',
        monthly_progression: '月度趋势',
        monthly_sub: '每月累计跑量 (公里)',
        monthly_count: '月度运动次数',
        monthly_count_sub: '每月运动次数统计',
        activity_profile: '运动构成',
        activity_sub: '按运动类型分布'
      },
      explorer: {
        header: '探索',
        moving: '移动中',
        heart_rate: '心率',
        cadence: '步频/踏频',
        climb: '爬升',
        training_load: '训练负荷',
        download_original: '原始文件',
        export_gpx: '导出 GPX'
      },
      import: {
        header: '数据',
        assets: '导入',
        sub: '同步您的多品牌运动数据',
        select_files: '选择 FIT, GPX 或 ZIP 文件',
        drag_drop: '拖拽文件到此处或点击浏览',
        initialize: '开始上传',
        processing: '正在处理...',
        results: '导入结果汇报'
      },
      detail: {
        distance: '距离',
        duration: '时长',
        pace: '配速',
        heart_rate: '心率',
        cadence: '步频',
        stride: '步幅',
        ascent: '爬升',
        calories: '卡路里',
        download_original: '原始文件',
        export_gpx: '导出 GPX',
        delete: '删除',
        confirm_delete_title: '确认删除',
        confirm_delete_msg: '此操作不可撤销，确定要删除这条运动记录吗？',
        cancel: '取消',
        confirm_delete: '确认删除'
      }
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    }
  });

export default i18n;
