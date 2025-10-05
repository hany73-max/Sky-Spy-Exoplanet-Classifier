import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from sklearn.calibration import calibration_curve
from cache_utils import get_model
import pandas as pd
import random

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

    st.title("📊 Data Exploration")

    # Load model and data
    model, le, features, df, (X_test, y_test) = get_model()

    # Drop unwanted columns (safety)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Sidebar controls
    st.sidebar.subheader("Visualization Controls")
    selected_features = st.sidebar.multiselect(
        "Select features for analysis:", features, default=features[:2]
    )
    sample_size = st.sidebar.slider("Sample size for scatter matrix:", 100, min(1000, len(df)), 500)

    # Class Distribution
    st.subheader("Class Distribution")
    df_copy = df.copy()
    df_copy["class"] = le.inverse_transform(df_copy["koi_disposition"])
    fig = px.histogram(df_copy, x="class", color="class",
                       title="Class Distribution: Confirmed vs False Positive",
                       labels={"class": "Class"},
                       color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)

    # Feature Importance
    st.subheader("Feature Importance")
    importances = model.named_steps['clf'].feature_importances_
    fig = px.bar(x=importances, y=features, orientation='h',
                 title="Feature Importance - Gradient Boosting",
                 labels={"x":"Importance", "y":"Feature"},
                 color=importances, color_continuous_scale="magma")
    st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    st.subheader("Feature Correlation Heatmap")
    corr = df[features].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis",
                    title="Feature Correlation Heatmap")
    st.plotly_chart(fig, use_container_width=True)

    # Feature Distributions
    st.subheader("Feature Distributions")
    for feat in selected_features:
        fig = px.histogram(df, x=feat, nbins=30, title=f"Distribution of {feat}")
        st.plotly_chart(fig, use_container_width=True)

    # Scatter Matrix
    st.subheader("Scatter Matrix")
    if len(selected_features) > 1:
        scatter_df = df.copy()
        scatter_df["class"] = le.inverse_transform(scatter_df["koi_disposition"]).astype(str)
        n_samples = min(sample_size, len(scatter_df))
        if n_samples < 2:
            st.warning("Not enough data for scatter matrix plot.")
        else:
            fig = px.scatter_matrix(scatter_df.sample(n=n_samples),
                                   dimensions=selected_features,
                                   color="class",
                                   title="Scatter Matrix of Selected Features")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least two features for scatter matrix.")

    # ROC Curve
    st.subheader("ROC Curve")
    y_proba = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                             name=f"AUC = {roc_auc:.2f}",
                             line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                             name="Random", line=dict(dash="dash")))
    fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate",
                      yaxis_title="True Positive Rate")
    st.plotly_chart(fig, use_container_width=True)

    # Precision-Recall Curve
    st.subheader("Precision-Recall Curve")
    prec, rec, _ = precision_recall_curve(y_test, y_proba)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rec, y=prec, mode="lines", line=dict(color="purple")))
    fig.update_layout(title="Precision-Recall Curve", xaxis_title="Recall", yaxis_title="Precision")
    st.plotly_chart(fig, use_container_width=True)

    # Calibration Curve
    st.subheader("Calibration Curve")
    prob_true, prob_pred = calibration_curve(y_test, y_proba, n_bins=10)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prob_pred, y=prob_true, mode="lines+markers", name="Model"))
    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                             name="Perfectly Calibrated", line=dict(dash="dash")))
    fig.update_layout(title="Calibration Curve", xaxis_title="Predicted Probability", yaxis_title="True Probability")
    st.plotly_chart(fig, use_container_width=True)

    # Data Overview
    st.subheader("Sample Data")
    st.dataframe(df.head(20))
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())
    st.subheader("Missing Values")
    missing = df.isnull().sum()
    st.dataframe(missing[missing > 0])