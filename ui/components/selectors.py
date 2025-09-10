import streamlit as st
from typing import List, Optional

def render_selectors(available_models: List[str], available_benchmarks: List[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Render selectors for model and benchmark. Accepts lists (can be empty).
    Returns (selected_model, selected_benchmark) or (None, None) if lists empty.
    """
    st.sidebar.header("Settings")

    if not available_models:
        st.sidebar.write("No models available")
        selected_model = None
    else:
        selected_model = st.sidebar.selectbox("Select model", available_models)

    if not available_benchmarks:
        st.sidebar.write("No benchmarks available")
        selected_benchmark = None
    else:
        selected_benchmark = st.sidebar.selectbox("Select benchmark", available_benchmarks)

    return selected_model, selected_benchmark
