import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import polyline

st.set_page_config(page_title="运动详情 - Nexus Sports", page_icon="🗺️", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("🗺️ 运动数据详情与轨迹")

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
            options = df.apply(lambda row: f"ID: {row['id']} | {row['开始时间']} | {row['activity_type']} | {row['distance_m']/1000:.2f}公里", axis=1).tolist()
            
            st.sidebar.markdown("### 选择运动记录")
            selected_option = st.sidebar.selectbox("浏览活动列表：", options)
            
            # Extract selected ID
            if selected_option:
                selected_id = int(selected_option.split(" | ")[0].replace("ID: ", ""))
                selected_activity = df[df['id'] == selected_id].iloc[0]
                
                # --- Top Metrics ---
                cols = st.columns(4)
                cols[0].metric("🏃 主要指标", f"{selected_activity['distance_m']/1000:.2f} 公里", f"{selected_activity['activity_type']}")
                cols[1].metric("⏱️ 时长", f"{selected_activity['duration_s']/60:.1f} 分钟")
                
                calories = selected_activity.get('calories_kcal')
                cols[2].metric("🔥 卡路里消耗", f"{calories:.0f} kcal" if pd.notna(calories) else "N/A")
                
                device = selected_activity.get('source_device', '未知设备')
                cols[3].metric("⌚ 数据来源", device)

                st.divider()

                # --- Map & Details Row ---
                map_col, det_col = st.columns([2, 1])
                
                with map_col:
                    poly_str = selected_activity.get('polyline')
                    if pd.notna(poly_str) and poly_str:
                        coordinates = polyline.decode(poly_str)
                        if coordinates:
                            # Start map centered at the first point
                            m = folium.Map(location=coordinates[0], zoom_start=13, tiles="cartodbpositron")
                            
                            # Draw polyline
                            folium.PolyLine(
                                coordinates,
                                weight=4,
                                color="blue",
                                opacity=0.8
                            ).add_to(m)
                            
                            # Add start and end markers
                            folium.Marker(coordinates[0], popup="Start", icon=folium.Icon(color="green", icon="play")).add_to(m)
                            folium.Marker(coordinates[-1], popup="End", icon=folium.Icon(color="red", icon="stop")).add_to(m)
                            
                            # Fit bounds to trace
                            m.fit_bounds(m.get_bounds())
                            
                            st_folium(m, width=700, height=500, returned_objects=[])
                        else:
                            st.warning("该记录的 GPS 坐标为空，无法绘制地图。")
                    else:
                        st.info("📌 该运动没有关联的 GPS 轨迹数据（可能是在室内或设备未记录）。")
                        
                with det_col:
                    st.subheader("📊 进阶指标")
                    
                    hr = selected_activity.get('avg_heart_rate')
                    st.write(f"**平均心率**：{f'{hr:.1f} bpm' if pd.notna(hr) else '无数据'}")
                    
                    cad = selected_activity.get('avg_cadence')
                    st.write(f"**平均步频**：{f'{cad:.1f} spm' if pd.notna(cad) else '无数据'}")
                    
                    stride = selected_activity.get('avg_stride_length_m')
                    st.write(f"**平均步幅**：{f'{stride:.2f} m' if pd.notna(stride) else '无数据'}")
                    
                    ascent = selected_activity.get('total_ascent_m')
                    st.write(f"**总爬升**：{f'{ascent:.1f} m' if pd.notna(ascent) else '无数据'}")
                    
                    st.divider()
                    st.subheader("🔋 生理分析")
                    
                    load = selected_activity.get('training_load')
                    st.write(f"**训练负荷**：{f'{load:.1f}' if pd.notna(load) else '无数据'}")
                    
                    rec = selected_activity.get('recovery_time_h')
                    st.write(f"**建议恢复时间**：{f'{rec:.1f} 小时' if pd.notna(rec) else '无数据'}")
                    
                    vo = selected_activity.get('vo2max')
                    st.write(f"**VO2 Max估算**：{f'{vo:.1f}' if pd.notna(vo) else '无数据'}")

    else:
        st.error("加载活动数据失败。")
except Exception as e:
    st.error(f"无法连接到后端服务: {e}")
