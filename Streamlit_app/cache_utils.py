# cache_utils.py
import streamlit as st
from model_utils import train_model

@st.cache_resource
def get_model():
    """Load and cache the model, label encoder, features, dataframe, and test data."""
    return train_model("exoplanets data_Set.csv", "exoplanets data_set 2.csv")
