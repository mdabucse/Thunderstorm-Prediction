import streamlit as st
from datetime import date

selected_date = st.date_input("Select a date", date.today())
st.write("You selected:", selected_date)
