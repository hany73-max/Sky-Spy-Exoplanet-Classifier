# 🔭 Sky-Spy: Exoplanet Candidate Classifier

Sky-Spy classifies candidate exoplanets from NASA's Kepler mission as either **CONFIRMED** exoplanets or **FALSE POSITIVES**, using a gradient-boosted classifier trained on orbital and stellar measurements from the Kepler Objects of Interest catalog.

Built for the NASA Space Apps Challenge 2025 by Team ExoExplorers.

### 🚀 [Live Demo](https://sky-spy-exoplanet-classifier-fieyq4vefydjeewt36jgnv.streamlit.app/)

---

## Overview

Kepler's mission flagged thousands of transit signals as exoplanet candidates, but many are false positives caused by noise, eclipsing binaries, or instrumental artifacts. Sky-Spy takes nine physical measurements of a candidate — orbital period, transit duration and depth, planetary radius, equilibrium temperature, insolation flux, and stellar temperature, surface gravity, and radius — and predicts whether it represents a confirmed planet or a false signal.

---

## Architecture

The system is split into a prediction API and a dashboard, deployed as two independent services.

```text
sky-spy-exoplanet-classifier/
│
├── app.py                    # Dashboard entry point and page router
├── api.py                    # FastAPI service — loads the model, serves /predict
├── cache_utils.py            # Streamlit session-level caching around model loading
├── requirements.txt
│
├── assets/                   # Dashboard images
├── data/                     # Kepler cumulative dataset (public NASA archive data)
├── models/                   # Serialized model and label encoder
├── notebooks/                # Exploratory analysis and prototyping
│
├── src/
│   └── model_utils.py         # Data loading, cleaning, and model training
│
└── view/
    ├── Home.py
    ├── Prediction.py          # Manual entry (via API) and CSV batch prediction (local)
    ├── DataExploration.py     # Class balance, correlations, feature distributions
    └── ModelPerformance.py    # Accuracy, confusion matrix, classification report
```

The dashboard's page router lives in `app.py` rather than using Streamlit's automatic `pages/` directory convention, to avoid conflicting with the app's own navigation.

---

## Features

- **Manual candidate classification** — enter a candidate's measurements directly and receive a prediction with confidence, served by the live API
- **Batch classification via CSV** — classify many candidates at once, with downloadable results
- **Data exploration dashboard** — class distribution, feature correlations, ROC, precision-recall, and calibration curves
- **Model performance reporting** — accuracy, confusion matrix, and classification report on held-out test data

---

## Model

- **Algorithm:** XGBoost classifier, tuned via grid search with 5-fold cross-validation
- **Features:** `koi_period`, `koi_duration`, `koi_depth`, `koi_prad`, `koi_teq`, `koi_insol`, `koi_steff`, `koi_slogg`, `koi_srad`
- **Target:** binary classification — CONFIRMED vs. FALSE POSITIVE
- **Scoring metric:** balanced accuracy

The trained model and label encoder are serialized to `models/` and loaded directly at runtime; training only re-runs if no saved model is present.

---

## Running Locally

```bash
git clone https://github.com/hany73-max/Sky-Spy-Exoplanet-Classifier.git
cd Sky-Spy-Exoplanet-Classifier
pip install -r requirements.txt
```

Start the API and dashboard in separate terminals:

```bash
uvicorn api:app --reload
streamlit run app.py
```

---

## Deployment

- **API** — deployed on Railway
- **Dashboard** — deployed on Streamlit Community Cloud, configured with an `API_URL` environment variable pointing to the deployed API

---

## Tech Stack

Python · XGBoost · scikit-learn · imbalanced-learn · FastAPI · Uvicorn · Streamlit · Plotly · Pandas · NumPy