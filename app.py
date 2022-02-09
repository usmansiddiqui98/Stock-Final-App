import streamlit as st
from multiapp import MultiApp
from apps import home, stock_final # import your application pages here

app = MultiApp()

st.sidebar.header('Navigation')
# Import all your application views here

app.add_app("About", home.app)
# app.add_app("Technical Analysis Indicators", data_stats.app)
app.add_app("Stock Analysis", stock_final.app)

# The main app
app.run()