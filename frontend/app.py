import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nexus Sports", page_icon="🏃", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("🏃 Nexus Sports - 运动数据统一管理")

# Sidebar navigation
st.sidebar.title("菜单")
page = st.sidebar.radio("选择页面", ["数据看板", "数据导入", "系统设置"])

if page == "数据看板":
    st.header("🏃‍♂️ 运动数据看板")
    try:
        resp = requests.get(f"{API_URL}/activities")
        if resp.status_code == 200:
            activities = resp.json()
            if not activities:
                st.info("未找到运动记录，请先导入数据。")
            else:
                st.metric("总运动次数", len(activities))
                
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
                    st.dataframe(df[display_cols], use_container_width=True)
                    
                    st.divider()
                    st.markdown("### 📥 数据导出与备份")
                    
                    export_row = st.columns([2, 1, 1, 5])
                    with export_row[0]:
                        selected_id = st.selectbox("选择要导出的运动记录ID", df['id'].tolist())
                    
                    if selected_id:
                        with export_row[1]:
                            st.link_button("导出原文件备份", f"{API_URL}/export/original/{selected_id}")
                        with export_row[2]:
                            st.link_button("导出基础GPX", f"{API_URL}/export/gpx/{selected_id}")
                        
        else:
            st.error("加载活动数据失败。")
    except Exception as e:
        st.error(f"无法连接到后端服务: {e}")

elif page == "数据导入":
    st.header("📤 数据导入")
    st.write("上传您的运动数据文件（支持 ZIP, FIT, GPX 格式）")
    uploaded_files = st.file_uploader("选择文件", accept_multiple_files=True, type=['zip', 'fit', 'gpx'])
    
    if st.button("开始上传") and uploaded_files:
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

elif page == "系统设置":
    st.header("⚙️ 系统设置")
    st.write("在此处进行系统参数配置（开发中）。")
