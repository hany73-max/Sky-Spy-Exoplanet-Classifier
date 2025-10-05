import os, csv
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


# ================== LOAD DATA ==================
def load_data(filepath):
    """Load CSV and drop junk columns like Unnamed:0."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    df = pd.read_csv(filepath, quoting=csv.QUOTE_ALL, comment="#")
    # Drop index-like columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


# ================== TRAIN MODEL ==================
@st.cache_data
def train_model(filepath_1, filepath_2=None):
    # Load datasets
    dataset_1 = load_data(filepath_1)
    if filepath_2:
        dataset_2 = load_data(filepath_2)
        df = pd.concat([dataset_1, dataset_2], ignore_index=True)
    else:
        df = dataset_1.copy()

    df.reset_index(drop=True, inplace=True)

    # Keep relevant cols
    df = df[features + [target]]
    df = df[df[target].isin(['CONFIRMED', 'FALSE POSITIVE'])]

    # Clean missing values
    df = df.dropna(subset=[target])
    df[features] = df[features].fillna(df[features].median())

    # Encode target
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )

    # ----------------- MODEL RUNNER -----------------
    def run_model(X_train, X_test, y_train, y_test,
                  estimator=None, grid_search=False,
                  grid_params=None, cv=None,
                  scoring="balanced_accuracy"):

        steps = [('clf', estimator)]
        pipe = Pipeline(steps=steps)

        if grid_search:
            model = GridSearchCV(
                pipe, param_grid=grid_params, cv=cv,
                scoring=scoring, n_jobs=-1
            )
        else:
            model = pipe

        with parallel_backend('threading', n_jobs=-1):
            model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        return model, y_pred

    # ----------------- TRAINING -----------------
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

    model, y_pred = run_model(
        X_train, X_test, y_train, y_test,
        estimator=XGBClassifier(
            random_state=42,
            eval_metric="logloss"
        ),
        grid_search=True,
        grid_params=params,
        cv=5,
        scoring="balanced_accuracy"
    )

    best_model = model.best_estimator_ if hasattr(model, "best_estimator_") else model

    # ----------------- REPORT -----------------
    print("\n📊 Best Params:", getattr(model, "best_params_", {}))
    print("\n📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))
    print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    return best_model, le, features, df, (X_test, y_test)


# ================== GET MODEL WRAPPER ==================
def get_model():
    """Wrapper to call in Streamlit app. Adjust file paths if needed."""
    return train_model("exoplanets data_Set.csv", "exoplanets data_set 2.csv")
