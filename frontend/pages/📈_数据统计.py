import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from ui_components import apply_cyber_theme, section_header, render_metric_card

st.set_page_config(page_title="数据统计 - Nexus Sports", page_icon="📈", layout="wide")

API_URL = "http://localhost:8000/api/v1"

# Apply Cyber Theme
apply_cyber_theme()

section_header("📈 数据统计分析", "深度透视您的活跃度与运动趋势")

# 1. Summary Metrics
try:
    resp = requests.get(f"{API_URL}/stats/summary")
    if resp.status_code == 200:
        stats_data = resp.json()
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_card("总计运动", f"{stats_data.get('total_activities', 0)} 次", "👟")
        with m2:
            render_metric_card("累计里程", f"{stats_data.get('total_distance_km', 0):.2f} km", "🏃", "green")
        with m3:
            render_metric_card("累计时长", f"{stats_data.get('total_duration_hours', 0):.1f} h", "⏱️")
        with m4:
            render_metric_card("消耗热量", f"{stats_data.get('total_calories_kcal', 0):.0f} kcal", "🔥", "green")
        
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.error("无法加载数据统计总览。")
except Exception as e:
    st.error(f"网络连接错误: {e}")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗓️ 月度里程趋势")
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
                    text='distance_km',
                    template="plotly_dark",
                    color_discrete_sequence=['#00F2FF']
                )
                fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("暂无趋势数据")
    except Exception as e:
        st.error(f"加载趋势错误: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 运动类型占比")
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
                    hole=0.6,
                    template="plotly_dark",
                    color_discrete_sequence=['#00F2FF', '#39FF14', '#FF00FF', '#FFFF00']
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("暂无分布数据")
    except Exception as e:
        st.error(f"加载分布错误: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
