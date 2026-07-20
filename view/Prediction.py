import streamlit as st
import pandas as pd
from cache_utils import get_model
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

    st.title("🚀 Exoplanet Prediction")

    # --- Load model and metadata ---
    model, le, features, df, (X_test, y_test) = get_model()

    # --- Selection: Manual or CSV Upload ---
    st.subheader("Choose Input Method")
    input_method = st.radio("Select how to provide data:", ["Manual Entry", "Upload CSV"])

    input_df = None
    if input_method == "Manual Entry":
        st.subheader("Enter Exoplanet Candidate Data")
        user_input = {feat: st.number_input(f"{feat}", value=0.0) for feat in features}
        input_df = pd.DataFrame([user_input], columns=features)

    else:
        st.subheader("Upload CSV File")
        uploaded_file = st.file_uploader("Upload a CSV file with candidate data", type=["csv"])
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
            input_df = input_df.loc[:, ~input_df.columns.str.contains("^Unnamed")]
            st.write("### Uploaded Data Preview")
            st.dataframe(input_df.head())
            input_df = input_df[features]

    # --- Prediction Button ---
    if st.button("Predict"):
        if input_df is None:
            st.warning("Please enter data or upload a valid CSV file.")
        else:
            preds = model.predict(input_df)
            labels = le.inverse_transform(preds)
            probas = model.predict_proba(input_df)

            if input_method == "Manual Entry":
                # Detailed report only for manual input
                st.subheader("📊 Prediction Report")
                st.success(f"### Prediction: {labels[0]}")
                st.write(f"Confidence: {probas.max():.2%}")

            else:
                # Show dataframe with predictions for CSV uploads
                st.subheader("✅ Predictions Completed")
                st.write(f"Predictions generated for {len(input_df)} candidates.")

                # Add prediction + confidence columns
                results_df = input_df.copy()
                results_df["Prediction"] = labels
                results_df["Confidence"] = probas.max(axis=1)

                # Show dataframe in app
                st.write("### Results with Predictions")
                st.dataframe(results_df)

                # Download option
                csv = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Predictions as CSV",
                    data=csv,
                    file_name="exoplanet_predictions.csv",
                    mime="text/csv",
                )
