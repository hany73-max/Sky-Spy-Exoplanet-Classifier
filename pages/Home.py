import streamlit as st
from PIL import Image
import requests
import base64
import random
from streamlit_lottie import st_lottie

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def run():
    st.set_page_config(page_title="Sky Spy", layout="wide", page_icon="🔭")

    # Load animations
    lottie_planet = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_gbfwtkzw.json")  
    lottie_ml = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json")      

    # Assets
    nasa_logo = "https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg"
    background_img_base64 = get_base64_of_bin_file("background.jpg")

    # ===== Animated Starfield Background =====
    star_count = 140
    stars_html = []
    for _ in range(star_count):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(0.6, 3.2)
        tw_dur = random.uniform(1.5, 3.5)
        drift_dur = random.uniform(8.0, 22.0)
        delay = random.uniform(0, 6)
        style = (
            f"top:{top:.2f}%; left:{left:.2f}%; "
            f"width:{size:.2f}px; height:{size:.2f}px; "
            f"animation: twinkle {tw_dur:.2f}s ease-in-out {delay:.2f}s infinite alternate, "
            f"drift {drift_dur:.2f}s linear {delay:.2f}s infinite;"
        )
        stars_html.append(f'<div class="star" style="{style}"></div>')
    stars_html = "".join(stars_html)

    # Background CSS and Animations
    st.markdown(
        f"""
        <style>
        .stApp {{ position: relative; background: transparent; }}
        #starfield {{ position: fixed; top:0; left:0; width:100%; height:100%; z-index:0; pointer-events:none; }}
        .star {{ position:absolute; background:white; border-radius:50%; box-shadow:0 0 6px rgba(255,255,255,0.9); opacity:0.85; }}
        @keyframes twinkle {{0%{{opacity:0.15;}}50%{{opacity:1;}}100%{{opacity:0.15;}}}}
        @keyframes drift {{0%{{transform:translateY(0px);}}50%{{transform:translateY(-10px);}}100%{{transform:translateY(0px);}}}}
        .stApp > div {{ position: relative; z-index: 2; }}

        /* Typing Effect */
        @keyframes typing {{ from {{ width: 0 }} to {{ width: 100% }} }}
        @keyframes blink {{ 50% {{ border-color: transparent }} }}
        .typing-text {{
            overflow: hidden;
            border-right: .15em solid #0b3d91;
            white-space: nowrap;
            animation: typing 3s steps(40, end), blink .75s step-end infinite;
            font-weight: 700; font-size: 1.5rem; color: #0b3d91;
        }}

        /* CTA cards */
        .cta-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 1rem;
        }}
        .cta-card:hover {{
            transform: translateY(-6px) scale(1.03);
            background: rgba(11,61,145,0.15);
        }}
        </style>
        <div id="starfield">{stars_html}</div>
        """,
        unsafe_allow_html=True,
    )

    # ===== Hero Section =====
    st.markdown(
        f"""
        <div style="position:relative; width:100%; height:420px; background:url('data:image/jpg;base64,{background_img_base64}') no-repeat center center; background-size:cover; filter:blur(3px);"></div>
        <div style="position:absolute; top:0; left:0; width:100%; height:420px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; background:rgba(0,0,0,0.25);">
            <img src="{nasa_logo}" width="120">
            <h1 style="color:#fff; font-size:3rem; font-weight:800;">Sky Spy</h1>
            <p class="typing-text">Exploring New Worlds Beyond Our Solar System 🚀</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===== Project Overview with Animation =====
    st.markdown("## 🌌 Why This Project Matters")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            Humanity has discovered **5,000+ exoplanets**, but many more candidates remain unconfirmed.  
            Using machine learning, this app helps scientists **separate real planets from false signals**.  

            ✨ With this tool, you can:  
            - Explore NASA TESS and Kepler’s rich dataset  
            - Visualize relationships between orbital and planetary features  
            - Test our ML model on new candidates  
            - Understand how AI can accelerate space discoveries  
            """
        )
    with col2:
        st_lottie(lottie_planet, height=250, key="planet")

    # ===== Fun Facts Section =====
    fun_facts = [
        "🌍 The first exoplanet was discovered in 1992 orbiting a pulsar.",
        "☀️ Some exoplanets orbit two suns, like Tatooine in Star Wars.",
        "🔥 'Hot Jupiters' are gas giants that orbit extremely close to their stars.",
        "💧 Finding Earth-like exoplanets increases the chance of finding life.",
        "🔭 Kepler discovered over 2,600 confirmed exoplanets in just 9 years."
    ]
    st.markdown("### 🌠 Did You Know?")
    st.info(random.choice(fun_facts))

    # ===== Interactive CTA Cards =====
    st.markdown("## 🚀 Get Started")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='cta-card'>🏠 <br> Home</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='cta-card'>🔮 <br> Prediction</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='cta-card'>📑 <br> Data Exploration</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='cta-card'>✅ <br> Model Performance</div>", unsafe_allow_html=True)

    # ===== ML Animation =====
    st.markdown("## 🛰️ How It Works")
    st_lottie(lottie_ml, height=200, key="ml")
    st.markdown(
        """
        Our model is built on a **XGBClassifier** trained on real data from NASA.  
        It learns subtle patterns in planetary radius, orbital period, temperature, and more.  
        With this, it can predict whether a candidate is a **CONFIRMED exoplanet** or a **FALSE POSITIVE**.  
        """
    )

    # Footer
    st.markdown("---")
    st.caption("🌌 Developed with ❤️ for NASA Space Apps Challenge 2025 by Team ExoExplorers")
