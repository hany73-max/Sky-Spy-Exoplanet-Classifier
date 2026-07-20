import streamlit as st
from cache_utils import get_model
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import plotly.figure_factory as ff
import pandas as pd
import random
import numpy as np

def run():
    # ===== Animated Starfield Background =====
    star_count = 140
    stars_html = []
    for _ in range(star_count):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(0.6, 3.2)  # px
        tw_dur = random.uniform(1.5, 3.5)  # twinkle duration
        drift_dur = random.uniform(8.0, 22.0)  # drift duration
        delay = random.uniform(0, 6)
        style = (
            f"top:{top:.2f}%; left:{left:.2f}%; "
            f"width:{size:.2f}px; height:{size:.2f}px; "
            f"animation: twinkle {tw_dur:.2f}s ease-in-out {delay:.2f}s infinite alternate, "
            f"drift {drift_dur:.2f}s linear {delay:.2f}s infinite;"
        )
        stars_html.append(f'<div class="star" style="{style}"></div>')

    stars_html = "".join(stars_html)

    st.markdown(
        f"""
        <style>
        .stApp {{
            position: relative;
            background: transparent;
        }}
        #starfield {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }}
        .star {{
            position: absolute;
            background: white;
            border-radius: 50%;
            box-shadow: 0 0 6px rgba(255,255,255,0.9);
            opacity: 0.85;
        }}
        @keyframes twinkle {{
            0% {{ opacity: 0.15; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.15; }}
        }}
        @keyframes drift {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        .stApp > div {{
            position: relative;
            z-index: 2;
        }}
        </style>
        <div id="starfield">{stars_html}</div>
        """,
        unsafe_allow_html=True,
    )

    # ===== Model Performance =====
    st.title("📈 Model Performance")

    # Load model and data
    model, le, features, df, (X_test, y_test) = get_model()
    y_pred = model.predict(X_test)

    # Accuracy
    st.subheader("Accuracy")
    st.metric("Test Accuracy", f"{accuracy_score(y_test, y_pred):.2%}")

    # Confusion Matrix
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    labels = le.inverse_transform([0, 1])  # map encoded labels back
    labels = [str(l) for l in labels]

    z_text = [[str(val) for val in row] for row in cm]
    fig = ff.create_annotated_heatmap(
        z=cm,
        x=labels,
        y=labels,
        annotation_text=z_text,
        colorscale="Viridis",
        showscale=True
    )
    fig.update_layout(
        title="Confusion Matrix",
        xaxis=dict(title="Predicted Label"),
        yaxis=dict(title="True Label")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Classification Report
    st.subheader("Classification Report")
    report = classification_report(
        y_test, y_pred, target_names=labels, output_dict=True
    )
    st.dataframe(pd.DataFrame(report).transpose())
