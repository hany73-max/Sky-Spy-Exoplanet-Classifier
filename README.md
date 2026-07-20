# 🔭 Sky-Spy: Exoplanet Candidate Classifier

**Sky-Spy** classifies candidate exoplanets from NASA's Kepler mission as either **CONFIRMED** exoplanets or **FALSE POSITIVES**, using an XGBoost model trained on real orbital and stellar measurements — from raw archive data, to a trained model, to a live, deployed prediction service with its own dashboard.

Originally built for the NASA Space Apps Challenge 2025 by Team ExoExplorers.

### 🚀 [Live Demo](https://sky-spy-exoplanet-classifier-fieyq4vefydjeewt36jgnv.streamlit.app/)

---

## 🧠 The Problem

Kepler's mission flagged thousands of "candidate" signals as possible exoplanets — but many are false positives caused by noise, eclipsing binaries, or instrument artifacts. Sky-Spy takes nine physical measurements of a candidate (orbital period, transit depth, planetary radius, stellar temperature, and more) and predicts whether it's a real confirmed planet or a false signal — the same kind of triage astronomers do manually, at scale.

---

## 🏗️ System Architecture

Same two-service split as this project's sister repo, [kessler-shield](https://github.com/hany73-max/kessler-shield) — a FastAPI backend that owns the model, and a Streamlit dashboard that only ever talks to it over HTTP, never touching the model directly for single predictions.

```text
sky-spy-exoplanet-classifier/
│
├── app.py                  # Entry point — manual page-switcher (not Streamlit's auto pages/)
├── api.py                  # FastAPI service — loads the model, serves /predict
├── cache_utils.py           # Session-level Streamlit caching wrapper around train_model()
├── requirements.txt
│
├── assets/                  # Images used across the dashboard (logo, backgrounds)
├── data/                    # Kepler cumulative dataset CSVs (public NASA archive data)
├── models/                  # Serialized champion_model.pkl + label_encoder.pkl
├── notebooks/                # Original EDA and prototyping
│
├── src/
│   └── model_utils.py        # Data loading, cleaning, training — trains once, then loads the saved model
│
└── view/
    ├── Home.py               # Landing page
    ├── Prediction.py         # Manual entry (via the API) + CSV batch (local) prediction
    ├── DataExploration.py    # EDA visualizations — class balance, correlations, feature distributions
    └── ModelPerformance.py   # Accuracy, confusion matrix, classification report
```

**Why `view/` and not `pages/`:** Streamlit auto-generates sidebar navigation from anything inside a folder literally named `pages/`. This app uses its own manual page-switcher in `app.py` instead — naming the folder `pages/` would have created two competing navigation systems fighting over the same sidebar.

---

## ✨ Features

- **Manual candidate entry** — enter a candidate's 9 measurements by hand, get an instant prediction with confidence, served by the live API
- **CSV batch classification** — upload many candidates at once, get predictions and confidence scores for all of them, downloadable as a results file
- **Data exploration dashboard** — class distribution, feature correlations, ROC/precision-recall/calibration curves, all interactive
- **Model performance page** — accuracy, confusion matrix, and full classification report against the held-out test set

---

## 🛠️ Running It Locally

```bash
git clone https://github.com/hany73-max/Sky-Spy-Exoplanet-Classifier.git
cd Sky-Spy-Exoplanet-Classifier
pip install -r requirements.txt
```

**Run the API and the dashboard** (two separate terminals):
```bash
uvicorn api:app --reload
streamlit run app.py
```

The first time `train_model()` runs with no saved model present, it performs a full `GridSearchCV` over the XGBoost hyperparameters — this is the slow path, and it only needs to happen once. After that, `models/champion_model.pkl` and `models/label_encoder.pkl` are loaded directly instead of retraining.

---

## 🚢 Deployment

- **API** (`api.py`) — deployed on Railway
- **Dashboard** (`app.py`) — deployed on Streamlit Community Cloud, configured via an `API_URL` secret pointing at the live API

---

## 📌 Known Limitations & Honest Notes

- CSV batch predictions run locally against the loaded model rather than through the API — sending hundreds of rows through a single-candidate HTTP endpoint one at a time would be slow. Only single manual predictions go through the deployed API.
- `data/` is intentionally committed to this repo (not gitignored) — unlike a private/licensed dataset, this is small, public NASA archive data the app genuinely needs at runtime to power the exploration and performance pages, not just for training.
- Filenames referenced in code are case-sensitive on the deployment host (Linux) even though local development happened on a case-insensitive filesystem (Windows) — worth double-checking exact filename casing against `src/model_utils.py` if you ever swap in a different data export.

---

## Built With

- **Python 3**
- **XGBoost** — gradient boosting classifier
- **scikit-learn / imbalanced-learn** — preprocessing, pipeline, label encoding
- **FastAPI + Uvicorn** — model-serving API
- **Streamlit + Plotly** — interactive dashboard
- **Pandas & NumPy** — data manipulation
