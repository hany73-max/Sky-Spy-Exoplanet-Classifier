import streamlit as st
import view.Home as Home
import view.Prediction as Prediction
import view.DataExploration as DataExploration
import view.ModelPerformance as ModelPerformance
import base64
import os
from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# App Config
st.set_page_config(
    page_title="Exoplanet Classifier",
    layout="wide",
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

# Helper: encode file to base64
def get_base64_of_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Files (update names if different)
image_file = ASSETS_DIR/"sidebar_bg.jpg"              

# quick existence checks (helps debugging)
if not os.path.exists(image_file):
    st.error(f"Sidebar image not found: {image_file}")
    # exit early so rest of code doesn't crash
    st.stop()


# encode files
img_base64 = get_base64_of_file(image_file)


# Sidebar background CSS
st.markdown(
   f"""
    <style>
        [data-testid="stSidebar"] {{
            position: relative;
            z-index: 0;
        }}
        [data-testid="stSidebar"]::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            filter: blur(8px);
            z-index: -1;
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
            position: relative;
            z-index: 1;
        }}
         
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar UI + single toggle button
with st.sidebar:
    st.image(ASSETS_DIR/ "logo.jpg", width=160)
    st.markdown("""
    ## Sky Spy  
    Classifying candidate exoplanets as **Confirmed** or **False Positive** using ML.
    """)
    st.markdown("[🔗 Data Source](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative)")
    st.markdown("---")

    # Page Navigation
    page = st.selectbox(
        "📂 Select a page:",
        ["Home", "Prediction", "Data Exploration", "Model Performance"]
    )

    st.markdown("---")
    st.caption("🚀 Developed by Team: **ExoExplorers**")


# Page mapping and run
PAGES = {
    "Home": Home,
    "Prediction": Prediction,
    "Data Exploration": DataExploration,
    "Model Performance": ModelPerformance
}

if page in PAGES:
    PAGES[page].run()
else:
    st.error("⚠️ Page not found. Please select a valid page.")
