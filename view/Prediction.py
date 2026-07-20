import streamlit as st
import pandas as pd
import requests
import os
import random
from cache_utils import get_model

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")


def predict_via_api(row: dict) -> dict:
    """Single-candidate path — this is the one that actually calls api.py."""
    response = requests.post(f"{API_URL}/predict", json=row)
    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"API error ({response.status_code}): {detail}")
    return response.json()


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
        .stApp {{ position: relative; background: transparent; }}
        #starfield {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }}
        .star {{ position: absolute; background: white; border-radius: 50%; box-shadow: 0 0 6px rgba(255,255,255,0.9); opacity: 0.85; }}
        @keyframes twinkle {{ 0% {{ opacity: 0.15; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.15; }} }}
        @keyframes drift {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }} }}
        .stApp > div {{ position: relative; z-index: 2; }}
        </style>
        <div id="starfield">{stars_html}</div>
        """,
        unsafe_allow_html=True,
    )

    st.title("🚀 Exoplanet Prediction")

    # CSV batch path still loads the model locally — sending hundreds of
    # rows through the API one at a time would be slow, same reasoning
    # as kessler-shield's batch tab.
    model, le, features, df, (X_test, y_test) = get_model()

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

    if st.button("Predict"):
        if input_df is None:
            st.warning("Please enter data or upload a valid CSV file.")

        elif input_method == "Manual Entry":
            # Single candidate — goes through the API
            try:
                result = predict_via_api(user_input)
            except requests.exceptions.ConnectionError:
                st.error(
                    "Couldn't reach the API. Make sure it's running:\n\n"
                    "`uvicorn api:app --reload`"
                )
                st.stop()
            except Exception as e:
                st.error(f"Prediction failed.\n\nDetails: {e}")
                st.stop()

            st.subheader("📊 Prediction Report")
            st.success(f"### Prediction: {result['prediction']}")
            st.write(f"Confidence: {result['confidence']:.2%}")

        else:
            # CSV batch — stays local, same model/le already loaded above
            preds = model.predict(input_df)
            labels = le.inverse_transform(preds)
            probas = model.predict_proba(input_df)

            st.subheader("✅ Predictions Completed")
            st.write(f"Predictions generated for {len(input_df)} candidates.")

            results_df = input_df.copy()
            results_df["Prediction"] = labels
            results_df["Confidence"] = probas.max(axis=1)

            st.write("### Results with Predictions")
            st.dataframe(results_df)

            csv = results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Predictions as CSV",
                data=csv,
                file_name="exoplanet_predictions.csv",
                mime="text/csv",
            )
