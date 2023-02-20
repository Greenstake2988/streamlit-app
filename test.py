import streamlit as st

col1, col2, col3 = st.beta_columns([3, 1, 3])

with col1:
    input1 = st.slider("Slider 1", 0, 100)

with col2:
    st.write("a")

with col3:
    input2 = st.slider("Slider 2", 0, 100)

