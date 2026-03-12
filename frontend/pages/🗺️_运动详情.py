import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import polyline
from frontend.ui_components import apply_cyber_theme, section_header, render_metric_card

st.set_page_config(page_title="运动详情 - Nexus Sports", page_icon="🗺️", layout="wide")

API_URL = "http://localhost:8000/api/v1"

# Apply theme
apply_cyber_theme()

section_header("🗺️ 运动轨迹详情", "探索您的运动地理足迹")

# Sidebar navigation
try:
    resp = requests.get(f"{API_URL}/activities")
    if resp.status_code == 200:
        activities = resp.json()
        if not activities:
            st.info("未找到运动记录，请先导入数据。")
        else:
            df = pd.DataFrame(activities)
            df['开始时间'] = pd.to_datetime(df['start_time']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Format display options for selectbox
            options = df.apply(lambda row: f"ID: {row['id']} | {row['开始时间']} | {row['activity_type']} | {row['distance_m']/1000:.2f}km", axis=1).tolist()
            
            st.sidebar.markdown("### 🔍 筛选活动")
            selected_option = st.sidebar.selectbox("浏览活动列表：", options, label_visibility="collapsed")
            
            # Extract selected ID
            if selected_option:
                selected_id = int(selected_option.split(" | ")[0].replace("ID: ", ""))
                selected_activity = df[df['id'] == selected_id].iloc[0]
                
                # --- Top Metrics Row ---
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    render_metric_card("距离", f"{selected_activity['distance_m']/1000:.2f} km", "🏃")
                with m2:
                    render_metric_card("配速", f"{selected_activity['activity_type']}", "👟", "green")
                with m3:
                    render_metric_card("运动时长", f"{selected_activity['duration_s']/60:.1f} min", "⏱️")
                with m4:
                    render_metric_card("数据来源", selected_activity.get('source_device', '未知设备'), "⌚", "green")

                st.markdown("<br>", unsafe_allow_html=True)

                # --- Map & Details Row ---
                map_col, det_col = st.columns([2.2, 1])
                
                with map_col:
                    poly_str = selected_activity.get('polyline')
                    if pd.notna(poly_str) and poly_str:
                        coordinates = polyline.decode(poly_str)
                        if coordinates:
                            # Start map centered at the first point
                            m = folium.Map(
                                location=coordinates[0], 
                                zoom_start=14, 
                                tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                                attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                            )
                            
                            # Draw polyline
                            folium.PolyLine(
                                coordinates,
                                weight=5,
                                color="#00F2FF",
                                opacity=0.9
                            ).add_to(m)
                            
                            # Add start and end markers with neon colors
                            folium.CircleMarker(coordinates[0], radius=8, color="#39FF14", fill=True, fill_color="#39FF14", popup="Start").add_to(m)
                            folium.CircleMarker(coordinates[-1], radius=8, color="#FF00FF", fill=True, fill_color="#FF00FF", popup="End").add_to(m)
                            
                            # Fit bounds
                            m.fit_bounds(m.get_bounds())
                            
                            st_folium(m, width=750, height=550, returned_objects=[], key=f"map_{selected_id}")
                        else:
                            st.warning("该记录的 GPS 坐标为空。")
                    else:
                        st.info("📌 该运动没有关联的 GPS 轨迹数据（可能是在室内或设备未记录）。")
                        
                with det_col:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("📊 进阶生理指标")
                    
                    def quick_stat(label, val, unit=""):
                        st.markdown(f"""
                        <div style="margin-bottom: 15px;">
                            <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">{label}</div>
                            <div style="color: white; font-size: 1.2rem; font-weight: 600;">{val} <span style="font-size: 0.8rem; color: #00F2FF;">{unit}</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                    hr = selected_activity.get('avg_heart_rate')
                    quick_stat("平均心率", f"{hr:.1f}" if pd.notna(hr) else "N/A", "bpm")
                    
                    cad = selected_activity.get('avg_cadence')
                    quick_stat("平均步频", f"{cad:.1f}" if pd.notna(cad) else "N/A", "spm")
                    
                    ascent = selected_activity.get('total_ascent_m')
                    quick_stat("总爬升", f"{ascent:.1f}" if pd.notna(ascent) else "N/A", "m")
                    
                    load = selected_activity.get('training_load')
                    quick_stat("训练负荷 (TL)", f"{load:.1f}" if pd.notna(load) else "N/A")

                    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                    
                    rec = selected_activity.get('recovery_time_h')
                    quick_stat("建议恢复时长", f"{rec:.1f}" if pd.notna(rec) else "N/A", "hours")
                    
                    vo = selected_activity.get('vo2max')
                    quick_stat("VO2 Max", f"{vo:.1f}" if pd.notna(vo) else "N/A")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("加载活动数据失败。")
except Exception as e:
    st.error(f"无法连接到后端服务: {e}")
