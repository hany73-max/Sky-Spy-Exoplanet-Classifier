# cache_utils.py
import streamlit as st
from pages.model_utils import train_model

@st.cache_resource
def get_model():
    """Load and cache the model, label encoder, features, dataframe, and test data."""
    return train_model("../data/exoplanets_data_Set.csv", "../data/exoplanets_data_set 2.csv")
