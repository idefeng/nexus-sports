import pandas as pd
from datetime import datetime
from frontend.ui_components import apply_cyber_theme, render_metric_card, section_header

st.set_page_config(page_title="Nexus Sports", page_icon="🏃", layout="wide")

API_URL = "http://localhost:8000/api/v1"

# Inject Global Cyber Theme CSS
apply_cyber_theme()

st.title("🏃 Nexus Sports")
st.markdown("---")

# Sidebar navigation
st.sidebar.markdown("# 🕹️ 控制中心")
page = st.sidebar.radio("请选择视图", ["📊 数据看板", "📤 数据导入", "⚙️ 系统设置"])

if page == "📊 数据看板":
    section_header("数据看板", "实时概览您的全量运动数据")
    try:
        resp = requests.get(f"{API_URL}/activities")
        if resp.status_code == 200:
            activities = resp.json()
            if not activities:
                st.info("未找到运动记录，请先导入数据。")
            else:
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    render_metric_card("总运动次数", f"{len(activities)}次", "👟")
                
                # Simple aggregate calculations
                df_calc = pd.DataFrame(activities)
                total_dist = df_calc['distance_m'].sum() / 1000
                total_dur = df_calc['duration_s'].sum() / 3600
                total_cal = df_calc['calories_kcal'].sum() if 'calories_kcal' in df_calc else 0
                
                with m2:
                    render_metric_card("累计距离", f"{total_dist:.2f}km", "📏", "green")
                with m3:
                    render_metric_card("累计时长", f"{total_dur:.1f}h", "⏱️")
                with m4:
                    render_metric_card("累计热量", f"{total_cal:.0f}kcal", "🔥", "green")
                
                st.markdown("<br>", unsafe_allow_html=True)
                section_header("历史记录明细")
                
                # Display simply for MVP
                df = pd.DataFrame(activities)
                if not df.empty:
                    df['start_time_raw'] = pd.to_datetime(df['start_time'])
                    df['开始时间'] = df['start_time_raw'].dt.strftime('%Y-%m-%d %H:%M')
                    df = df.rename(columns={
                        'activity_type': '运动类型',
                        'distance_m': '距离 (米)',
                        'duration_s': '时长 (秒)',
                        'source_device': '数据来源'
                    })
                    display_cols = ['id', '开始时间', '运动类型', '距离 (米)', '时长 (秒)', '数据来源']
                    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    section_header("数据导出与备份", "将您的运动资产导出为标准格式")
                    
                    with st.container():
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        export_row = st.columns([1, 1, 1, 3])
                        with export_row[0]:
                            selected_id = st.selectbox("选择 ID", df['id'].tolist(), label_visibility="collapsed")
                        
                        if selected_id:
                            with export_row[1]:
                                st.link_button("💾 原始备份", f"{API_URL}/export/original/{selected_id}", use_container_width=True)
                            with export_row[2]:
                                st.link_button("🌍 导出 GPX", f"{API_URL}/export/gpx/{selected_id}", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
        else:
            st.error("加载活动数据失败。")
    except Exception as e:
        st.error(f"无法连接到后端服务: {e}")

elif page == "📤 数据导入":
    section_header("数据导入", "支持跨品牌数据的极速解析")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("请上传您的 ZIP, FIT 或 GPX 格式文件：")
    uploaded_files = st.file_uploader("选择文件", accept_multiple_files=True, type=['zip', 'fit', 'gpx'], label_visibility="collapsed")
    
    if st.button("🚀 开始极速解析") and uploaded_files:
        with st.spinner("正在上传并解析文件..."):
            files_to_upload = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
            
            try:
                resp = requests.post(f"{API_URL}/upload", files=files_to_upload)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    for res in results:
                        if res['status'] == 'success':
                            st.success(f"{res['filename']}: {res['message']} (成功导入 {res.get('activities_imported', 0)} 条记录)")
                        elif res['status'] == 'skipped':
                            st.info(f"{res['filename']}: {res['message']}")
                        else:
                            st.error(f"{res['filename']}: {res.get('message', '未知错误')}")
                else:
                    st.error("上传失败。")
            except Exception as e:
                st.error(f"网络连接错误: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚙️ 系统设置":
    section_header("系统设置")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("在此处进行系统参数配置（开发中）。")
    st.markdown('</div>', unsafe_allow_html=True)
