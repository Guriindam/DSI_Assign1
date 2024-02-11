
import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt


df = pd.read_csv("Salary.csv")
st.title("Salary across different demographics")

with st.sidebar.form("MONEY"):
    st.sidebar.header("Select Filter of Choosing:")
    selected_x_var = st.sidebar.selectbox("x variable", df.columns)
    selected_y_var = st.sidebar.selectbox("y variable",df.columns)
    st.form_submit_button("submit")

#Bar Chart of Job Titles

jobtitle_count = df["Job Title"].value_counts().reset_index()
jobtitle_count.columns = ['Job Title', 'Count']
popular_job = jobtitle_count.loc[jobtitle_count["Count"].idxmax(), 'Job Title']

fig = alt.Chart(jobtitle_count).mark_bar().encode(
    x='Job Title:O',
    y="Count:Q",
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum["Job Title"] == popular_job,
        alt.value('orange'),    
        alt.value('steelblue')   
    )
).properties(width=600)

st.altair_chart(fig)