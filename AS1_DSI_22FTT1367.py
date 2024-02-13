
import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure

df = pd.read_csv("Salary.csv")
st.title("Salary across different demographics")

with st.sidebar:
    with st.form('money'):
        st.header("Select Filter of Choosing:")
        selected_x_var = st.selectbox("x variable", df.columns)
        selected_y_var = st.selectbox("y variable", df["Job Title"].unique())
        st.form_submit_button("submit") 

    filtered_job = df[df["Job Title"] == selected_y_var]
        

with st.container():
        
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
    )

    st.altair_chart(fig, use_container_width= True)


with st.container():

    chart = alt.Chart(filtered_job).mark_point().encode(
        x=alt.X('Age', title='Age'),
        y=alt.Y(selected_x_var, title=selected_x_var),
    ).properties(width=500)

    st.altair_chart(chart)  
    #Gender Male Female Pie Chart


with st.container():

    gender_count = df["Gender"].value_counts().reset_index()
    base = alt.Chart(gender_count).encode(
        alt.Theta("Gender:Q").stack(True),
        alt.Color("Gender:N").legend(None)
    )

    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=140, size=20).encode(text="Gender:N")

    pie + text

