import streamlit as st
from config import APP_TITLE

def render_header():
    st.title(APP_TITLE)
    st.markdown(
        'Interactive dashboard to compare model forecasts actual data and benchmark.'
        'Data is loaded from "shared volume", in future from Prediction API'
    )
    st.markdown('---')
