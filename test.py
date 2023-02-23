import streamlit as st

options = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

default_option = ""

selected_option = st.selectbox("Select an option", [default_option] + options, key="selectbox")

if selected_option == default_option:
    typed_value = st.text_input("Type an option")
    selected_option = typed_value.lower() if typed_value.lower() in map(str.lower, options) else default_option

st.write("You selected:", selected_option)
