###################Causal Dashboard###################
#Author: David Guillaume
#Date: 2024-09-14
#Version: 0.1
#Description: Create a web dashboard, displaying the result of different causal analysis


import streamlit as st # type: ignore
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import (check_X_y, check_array, check_is_fitted)
import cvxpy as cp
from methods.SCM import analyse
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
     page_title='Caussal Dashboard',
     page_icon='➡️',
     layout='wide',
     initial_sidebar_state='expanded')

# Title of the app
st.title('Causal Dashboard')

sc = None
result = None
att = None
df_weights = None


# Sidebar
with st.sidebar:
    st.title('Analysis settings')


    st.text("The CSV file must have the first column \n as the unit and the rest of columns as years,\n like on the picture below.")
    st.image("assets\example.png", caption="Your csv file should have a similar format", use_column_width=True)

    #selector for the separator
    options = [";", ","]

    # Create a selectbox
    separator = st.selectbox("Choose a type of separator", options)

    # Add file uploader to allow CSV uploads
    uploaded_file = st.file_uploader("Choose a CSV file.", type="csv")





    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file, sep=separator, index_col=0)
        
        # Display the DataFrame
        st.write("File uploaded successfully:", uploaded_file.name)

            

        #treated
        treateds = df.index
        treated = st.selectbox("Select the treated variable", treateds)

        #Treatment year
        treatment_years = df.columns
        treatment_years = treatment_years[1:-1]    #thus they can't select the first and last year
        treatment_year = int(st.selectbox("Select the treatment year", treatment_years))

        submitted = st.button("Run the analysis")

        if submitted:
            sc, result, att, df_weights = analyse(df=df, treated=treated, treatment_year=treatment_year)

    else:
        st.write("No file uploaded.")

# Function to plot data and add vertical line
def plot_data(result, treatment_year=None):
    plt.figure(figsize=(10, 5))
    # Plot two lines, one for each column
    sns.lineplot(x=result.index, y=result['Treated'], label=f"Treated: {treated}")
    sns.lineplot(x=result.index, y=result['Synthetic Control'], label='Synthetic Control')

    # Add labels and a legend
    plt.xlabel('Time')
    plt.ylabel('GDP per capita')
    plt.axvline(x=treatment_year, color='red', linestyle='--', label='2020')
    plt.legend()

    # Use Streamlit to display the plot
    st.pyplot(plt)
    plt.clf()  # Clear the figure after plotting

if sc is not None:
    col1, col2, col3 = st.columns([0.5, 0.25, 0.25])  # Adjust width ratio (2 gives more space to the graph)

    # Display content in the first two columns
    with col1:
        st.write("Plot of the Synthetic Control and the Treated")
        plot_data(result, treatment_year=treatment_year)

    with col2:
        st.write("Weights to create the Synthetic Control")
        st.dataframe(df_weights.sort_values(by='weight', ascending=False))

    with col3:
        st.write("Effect per year")
        st.dataframe(att)

else:
    st.text("No data to display")
    
    


