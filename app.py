import streamlit as st
import pandas as pd
from backend.config import ROOMS, DEFAULT_SETTINGS
from backend.occupancy import get_occupancy
from backend.control import calculate_controls
from backend.energy import energy_summary, weekly_report
from backend.recommendations import recommendations
from frontend.ui import (render_sidebar, render_dashboard, render_weekly_report, render_recommendations)

st.set_page_config(page_title="Smart Classroom | DSU Code Clash 2.0", page_icon="⚡", layout="wide")

st.markdown("""
<style>
/* ===== MAIN BACKGROUND ===== */
.stApp {
    background: #EDF3FB !important;
    color: #172B4D !important;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* ===== MAIN HEADINGS ===== */
h1, h2, h3, h4, h5 {
    color: #12305A !important;
    font-weight: 750 !important;
}

/* ===== BODY TEXT ===== */
p, li, label,
[data-testid="stCaptionContainer"] {
    color: #304563 !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #DCE9FA !important;
    border-right: 1px solid #B7CBE8;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: #17365D !important;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #D0DDEE !important;
    border-radius: 14px !important;
    padding: 18px !important;
    box-shadow: 0 4px 14px rgba(24, 55, 96, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #425875 !important;
}

[data-testid="stMetricValue"] {
    color: #075BC7 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #087F5B !important;
}

/* ===== BUTTONS ===== */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    background: #1769D2 !important;
    color: #FFFFFF !important;
    border: 1px solid #1769D2 !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
    padding: 0.5rem 1rem !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #104FA5 !important;
    border-color: #104FA5 !important;
    color: #FFFFFF !important;
}

/* ===== TEXT INPUTS ===== */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #172B4D !important;
    border: 1px solid #9FB5D3 !important;
    border-radius: 8px !important;
}

/* ===== SELECT BOXES ===== */
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172B4D !important;
    border-color: #9FB5D3 !important;
}

/* Dropdown menu options */
[role="option"] {
    background: #FFFFFF !important;
    color: #172B4D !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: #DCE8F8 !important;
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    color: #304563 !important;
}

.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #075BC7 !important;
    font-weight: 750 !important;
    border-bottom: 3px solid #1769D2 !important;
}

/* ===== EXPANDERS & CARDS ===== */
[data-testid="stExpander"],
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #D0DDEE;
    border-radius: 12px;
}

/* ===== ALERTS ===== */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ===== TABLES ===== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF !important;
    border: 1px solid #D0DDEE;
    border-radius: 10px;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #C7D6EA !important;
}

/* ===== CHECKBOXES & RADIO BUTTONS ===== */
.stCheckbox label,
.stRadio label {
    color: #243B5A !important;
}

/* ===== CHART CONTAINERS ===== */
[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: #FFFFFF;
    border: 1px solid #D0DDEE;
    border-radius: 12px;
    padding: 8px;
}

/* ===== MOBILE SPACING ===== */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.7rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


st.title("⚡ Smart Classroom Automation")
st.caption("DSU Code Clash 2.0 • Energy-aware classroom operations • Simulation-first prototype")

settings = render_sidebar(DEFAULT_SETTINGS, ROOMS)
room_name = settings["room"]
room = ROOMS[room_name]

with st.sidebar:
    st.markdown("---")
    

occupancy, camera_status, camera_note = get_occupancy(
    source=settings["camera_source"],
    mode=settings["occupancy_mode"],
    simulated_count=settings["simulated_occupancy"],
    capacity=room["capacity"],
    camera_index=settings["camera_index"]
)
controls = calculate_controls(room, settings, occupancy)
summary = energy_summary(room, controls, settings)
render_dashboard(room_name, room, occupancy, camera_status, camera_note, settings, controls, summary)

st.markdown("---")
render_weekly_report(weekly_report(room, settings))
st.markdown("---")
render_recommendations(recommendations(occupancy, settings, controls, summary))

with st.expander("🧪 Diagnostics & implementation notes"):
    st.write("**Occupancy source:**", camera_status, "—", camera_note)
    st.write("**Control mode:** Simulation only")
    st.write("**Lighting logic:** occupancy, daylight, projection mode, manual override and brightness bounds are combined in backend/control.py.")
    st.write("**Energy estimate:** device wattages × hours ÷ 1000. Weekly data is clearly labelled as illustrative demo data.")
    st.write("**Safety:** Camera/sensor errors fall back to a safe simulated state; check occupancy manually if the camera is unavailable.")
