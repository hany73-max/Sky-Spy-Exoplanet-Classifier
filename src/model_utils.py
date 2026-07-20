import os, csv
from pathlib import Path
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline
from joblib import parallel_backend
import streamlit as st

# ================== CONFIG ==================
features = [
    'koi_period', 'koi_duration', 'koi_depth', 'koi_prad',
    'koi_teq', 'koi_insol', 'koi_steff', 'koi_slogg', 'koi_srad'
]
target = "koi_disposition"

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODELS_DIR / "champion_model.pkl"
ENCODER_PATH = MODELS_DIR / "label_encoder.pkl"


# ================== LOAD DATA ==================
def load_data(filepath):
    """Load CSV and drop junk columns like Unnamed:0."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    df = pd.read_csv(filepath, quoting=csv.QUOTE_ALL, comment="#")
    # Drop index-like columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


# ================== GRID SEARCH (only runs when no cached model exists) ==
def _run_grid_search(X_train, y_train):
    params = {
        'clf__n_estimators': [800],
        "clf__learning_rate": [0.15],
        'clf__max_depth': [4],
        "clf__subsample": [1],
        "clf__colsample_bytree": [1],
        "clf__min_child_weight": [1],
        "clf__gamma": [0.2],
        "clf__reg_alpha": [0],
        "clf__reg_lambda": [1.0]
    }

    pipe = Pipeline(steps=[(
        'clf', XGBClassifier(random_state=42, eval_metric="logloss")
    )])

    model = GridSearchCV(
        pipe, param_grid=params, cv=5,
        scoring="balanced_accuracy", n_jobs=-1
    )

    with parallel_backend('threading', n_jobs=-1):
        model.fit(X_train, y_train)

    return model


# ================== TRAIN OR LOAD MODEL ==================
@st.cache_data
def train_model(filepath_1, filepath_2=None):
    # --- Load + clean data (cheap, always runs) ---
    dataset_1 = load_data(filepath_1)
    if filepath_2:
        dataset_2 = load_data(filepath_2)
        df = pd.concat([dataset_1, dataset_2], ignore_index=True)
    else:
        df = dataset_1.copy()

    df.reset_index(drop=True, inplace=True)
    df = df[features + [target]]
    df = df[df[target].isin(['CONFIRMED', 'FALSE POSITIVE'])]
    df = df.dropna(subset=[target])
    df[features] = df[features].fillna(df[features].median())

    cache_exists = MODEL_PATH.exists() and ENCODER_PATH.exists()

    if cache_exists:
        # --- Fast path: load the already-trained model + the exact
        # label encoder it was trained with, skip GridSearchCV entirely ---
        best_model = joblib.load(MODEL_PATH)
        le = joblib.load(ENCODER_PATH)
        df[target] = le.transform(df[target])
    else:
        # --- Slow path: only runs once, then gets committed to the repo ---
        le = LabelEncoder()
        df[target] = le.fit_transform(df[target])

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )

    if not cache_exists:
        model = _run_grid_search(X_train, y_train)
        best_model = model.best_estimator_ if hasattr(model, "best_estimator_") else model

        y_pred = best_model.predict(X_test)
        print("\n📊 Best Params:", getattr(model, "best_params_", {}))
        print("\n📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))
        print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_model, MODEL_PATH)
        joblib.dump(le, ENCODER_PATH)
        print(f"✅ Saved trained model to {MODEL_PATH}")

    return best_model, le, features, df, (X_test, y_test)
