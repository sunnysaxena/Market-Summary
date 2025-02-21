import streamlit as st

def show_loader():
    """
    Display an elegant loading animation
    """
    with st.spinner('Loading data...'):
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
        progress_bar.empty()
