import streamlit as st

def apply_cyber_theme():
    """Injects custom CSS to achieve a professional 'Cyber Sports' dark theme."""
    cyber_css = """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap');
    
    :root {
        --cyber-bg: #0E1117;
        --cyber-cyan: #00F2FF;
        --cyber-green: #39FF14;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--cyber-bg);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Containers */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid var(--cyber-cyan);
    }

    /* Metric Cards Custom Styling */
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--cyber-cyan);
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0d11;
        border-right: 1px solid var(--glass-border);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.6) !important;
        transform: scale(1.02) !important;
    }

    /* Dataframe custom look */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid var(--glass-border);
    }

    /* Hide standard header */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """
    st.markdown(cyber_css, unsafe_allow_html=True)

def render_metric_card(label, value, icon, color_theme="cyan"):
    """Renders a custom HTML metric card with glassmorphism."""
    color = "#00F2FF" if color_theme == "cyan" else "#39FF14"
    bg_shadow = "rgba(0, 242, 255, 0.2)" if color_theme == "cyan" else "rgba(57, 255, 20, 0.2)"
    
    html = f"""
    <div class="glass-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color}; text-shadow: 0 0 10px {bg_shadow};">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    """Renders a professional section header."""
    st.markdown(f"""
        <div style="margin-top: 2rem; margin-bottom: 1rem;">
            <h2 style="color: white; font-weight: 800; margin-bottom: 0;">{title}</h2>
            {f'<p style="color: rgba(255,255,255,0.5); margin-top: 0;">{subtitle}</p>' if subtitle else ''}
            <div style="height: 3px; width: 50px; background: linear-gradient(90deg, #00F2FF, transparent); border-radius: 3px;"></div>
        </div>
    """, unsafe_allow_html=True)
