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
        total_sessions: 'Total Sessions',
        cumulative_distance: 'Cumulative Distance',
        training_time: 'Training Time',
        active_calories: 'Active Calories',
        recent_activities: 'Recent Activities',
        view_all: 'View All',
        ai_analysis: 'AI Analysis',
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
        kcal: 'kcal'
      },
      stats: {
        header: 'Analytics',
        insights: 'Insights',
        sub: 'Advanced data visualization & trend analysis',
        monthly_progression: 'Monthly Progression',
        monthly_sub: 'Distance accumulated per month (km)',
        activity_profile: 'Activity Profile',
        activity_sub: 'Distribution by exercise type'
      },
      explorer: {
        header: 'Explorer',
        moving: 'Moving',
        heart_rate: 'Heart Rate',
        cadence: 'Cadence',
        climb: 'Climb',
        training_load: 'Training Load'
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
        total_sessions: '总运动次数',
        cumulative_distance: '累计距离',
        training_time: '累计时长',
        active_calories: '活动消耗',
        recent_activities: '最近运动记录',
        view_all: '查看全部',
        ai_analysis: 'AI 深度分析',
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
        kcal: '千卡'
      },
      stats: {
        header: '分析',
        insights: '洞察',
        sub: '进阶数据可视化与趋势分析',
        monthly_progression: '月度趋势',
        monthly_sub: '每月累计跑量 (公里)',
        activity_profile: '运动构成',
        activity_sub: '按运动类型分布'
      },
      explorer: {
        header: '探索',
        moving: '移动中',
        heart_rate: '心率',
        cadence: '步频/踏频',
        climb: '爬升',
        training_load: '训练负荷'
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
