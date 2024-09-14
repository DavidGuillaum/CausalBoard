###################Causal Dashboard###################
#Author: David Guillaume
#Date: 2024-09-14
#Version: 0.1
#Description: Create a web dashboard, displaying the result of different causal analysis


import streamlit as st # type: ignore


# Page configuration
st.set_page_config(
     page_title='Caussal Dashboard',
     page_icon='➡️',
     layout='wide',
     initial_sidebar_state='expanded')

# Title of the app
st.title('Causal Dashboard')

# Sidebar
st.sidebar.subheader('Analysis settings')

