import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="数据统计 - Nexus Sports", page_icon="📈", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("📈 数据统计分析")

# 1. Summary Metrics
try:
    resp = requests.get(f"{API_URL}/stats/summary")
    if resp.status_code == 200:
        stats_data = resp.json()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总计运动次数", f"{stats_data.get('total_activities', 0)} 次")
        with col2:
            st.metric("总计里程", f"{stats_data.get('total_distance_km', 0):.2f} 公里")
        with col3:
            st.metric("总计用时", f"{stats_data.get('total_duration_hours', 0):.1f} 小时")
        with col4:
            st.metric("消耗热量", f"{stats_data.get('total_calories_kcal', 0):.0f} 千卡")
        
        st.divider()
    else:
        st.error("无法加载数据统计总览。")
except Exception as e:
    st.error(f"网络连接错误: {e}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("月度跑量趋势")
    try:
        trend_resp = requests.get(f"{API_URL}/stats/trend")
        if trend_resp.status_code == 200:
            trend_data = trend_resp.json().get("trends", [])
            if trend_data:
                df_trend = pd.DataFrame(trend_data)
                fig = px.bar(
                    df_trend, 
                    x='month', 
                    y='distance_km', 
                    labels={'month': '月份', 'distance_km': '里程 (公里)'},
                    text='distance_km'
                )
                fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("暂无趋势数据")
    except Exception as e:
        st.error(f"加载趋势错误: {e}")

with col2:
    st.subheader("运动类型分布")
    try:
        dist_resp = requests.get(f"{API_URL}/stats/distribution")
        if dist_resp.status_code == 200:
            dist_data = dist_resp.json().get("distribution", [])
            if dist_data:
                df_dist = pd.DataFrame(dist_data)
                fig_pie = px.pie(
                    df_dist, 
                    names='type', 
                    values='count', 
                    hole=0.4
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("暂无分布数据")
    except Exception as e:
        st.error(f"加载分布错误: {e}")
