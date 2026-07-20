from fastapi import FastAPI, HTTPException
from pathlib import Path
from pydantic import BaseModel
import pandas as pd
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent  # api.py sits at repo root
MODELS_DIR = PROJECT_ROOT / "models"

model = joblib.load(MODELS_DIR / "champion_model.pkl")
le = joblib.load(MODELS_DIR / "label_encoder.pkl")

app = FastAPI()

FEATURES = [
    'koi_period', 'koi_duration', 'koi_depth', 'koi_prad',
    'koi_teq', 'koi_insol', 'koi_steff', 'koi_slogg', 'koi_srad'
]


class ExoplanetCandidate(BaseModel):
    koi_period: float
    koi_duration: float
    koi_depth: float
    koi_prad: float
    koi_teq: float
    koi_insol: float
    koi_steff: float
    koi_slogg: float
    koi_srad: float


@app.post("/predict")
def predict(candidate: ExoplanetCandidate):
    try:
        input_df = pd.DataFrame([candidate.dict()])[FEATURES]  # enforce column order
        pred = model.predict(input_df)
        label = le.inverse_transform(pred)[0]
        confidence = float(model.predict_proba(input_df).max())

        return {
            "prediction": str(label),
            "confidence": confidence,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
