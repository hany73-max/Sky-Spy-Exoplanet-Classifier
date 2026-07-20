# cache_utils.py
import streamlit as st
from pathlib import Path
from src.model_utils import train_model

DATA_DIR = Path(__file__).resolve().parent / "data"


@st.cache_resource
def get_model():
    return train_model(DATA_DIR / "exoplanets_data_Set.csv", DATA_DIR / "exoplanets_data_set 2.csv")
