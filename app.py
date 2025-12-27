import streamlit as st
import pandas as pd
import io
import os
from dotenv import load_dotenv

# 1. Load Environment Variables First
load_dotenv()

# 2. Imports from your source modules
from src.data_processor import process_csv
from src.agent_engine import get_ai_insight

st.set_page_config(page_title="AI Report Gen", layout="wide")

# --- 🚀 TURBO MODE: CACHING WRAPPER ---
# This saves the result of the AI call. If the inputs (stats + type) 
# don't change, it returns the previous answer instantly.
@st.cache_data(show_spinner=False)
def get_cached_insight(stats, insight_type):
    """
    Wrapper to cache AI responses for instant retrieval on re-runs.
    """
    return get_ai_insight(stats, insight_type)
# --------------------------------------
st.markdown("""
<style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1f1f1f 25%, #4b5563 50%, #d1d5db 75%, #ffffff 100%);
    }
    
    /* Main content card */
    .main-card {
    margin: 1rem auto; /* Decrease the first number (1rem) to move the box higher */
    padding: 2rem;     /* Decrease this to make the internal space tighter */
    /* ... other styles ... */
    }
    
    /* Typography */
    .main-title {
        background: linear-gradient(90deg, #e0d6d8, #ff6347, #FF795E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    .file-badge {
        display: inline-block;
        background: linear-gradient(90deg, #FFAE09, #7AF089);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Results area */
    .results-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        border-left: 6px solid;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
        animation: fadeIn 0.5s ease;
        color: #1e293b;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Expander styling fix */
    .st-expander-header p {
        color: #ff6347 !important;
        font-weight: 600 !important;
    }

    /* Markdown headings */
    .stMarkdown h3 {
        color: #4865F6 !important;
    }
    
    /* Button refinement */
    .stButton button {
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)


st.title("AI Workflow & Report Generator")
st.markdown("### ⚡ Instant Business Analytics")


# Initialize session state for stats_dict
if 'stats_dict' not in st.session_state:
    st.session_state['stats_dict'] = None

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Check if this is a new file to avoid re-processing on every interaction
    # (We use size + name as a proxy for file_id if file_id isn't available)
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    
    if st.session_state['stats_dict'] is None or file_id != st.session_state.get('uploaded_file_id'):
        try:
            # Process the CSV (Pandas Math - Fast)
            st.session_state['stats_dict'] = process_csv(io.BytesIO(uploaded_file.getvalue()))
            st.session_state['uploaded_file_id'] = file_id 
            st.success("✅ CSV processed successfully!")
            
            # Optional: Clear cache if new data comes in
            get_cached_insight.clear()
            
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.info("Please ensure you upload a valid CSV file.")
            st.session_state['stats_dict'] = None
            st.session_state['uploaded_file_id'] = None

# Display Interface if Data is Ready
if st.session_state['stats_dict'] is not None:
    stats_dict = st.session_state['stats_dict']

    st.divider()
    st.subheader("Generate AI Insights")

    # Create three columns for buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📈 Summarize Trends", use_container_width=True):
            with st.spinner("Analyzing Trends..."):
                # CALL THE CACHED FUNCTION
                trend_insight = get_cached_insight(stats_dict, "Trends")
                st.info("### Trends Insight")
                st.write(trend_insight)

    with col2:
        if st.button("⚠️ Identify Anomalies", use_container_width=True):
            with st.spinner("Scanning for Anomalies..."):
                # CALL THE CACHED FUNCTION
                anomaly_insight = get_cached_insight(stats_dict, "Anomalies")
                st.warning("### Anomalies Insight")
                st.write(anomaly_insight)

    with col3:
        if st.button("🚀 Strategic Actions", use_container_width=True):
            with st.spinner("Formulating Strategy..."):
                # CALL THE CACHED FUNCTION
                action_insight = get_cached_insight(stats_dict, "Actions")
                st.success("### Strategic Actions")
                st.write(action_insight)
else:
    st.info("Please upload a CSV file to get started.")
