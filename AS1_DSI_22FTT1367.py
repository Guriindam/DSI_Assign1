
import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.express as px



df = pd.read_csv("Salary.csv")
#st.title("Salary Across Different Demographics")
job_title_counts = df['Job Title'].value_counts()
#st.write(job_title_counts)

#Removing job columns that only have 10 or less rows
job1 = job_title_counts[job_title_counts <= 10].index
# The ~ acts as a boolean button
filtered_df = df[~df['Job Title'].isin(job1)]

job_title_new_count = filtered_df['Job Title'].value_counts()



#Filters
with st.sidebar:
    with st.form('Filters'):
        st.header("Select Filter of Choosing:")
        selected_job = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())
        selected_gender = st.selectbox("Select Gender", filtered_df['Gender'].unique())
        selected_race = st.multiselect("Select Race :smiling_imp:", filtered_df["Race"].unique())
        st.form_submit_button("submit") 
        
    filtered_job_gender = filtered_df[(filtered_df["Gender"] == selected_gender) & (filtered_df['Job Title'] == selected_job)]
    filtered_job = filtered_df[filtered_df["Job Title"] == selected_job]
    filtered_race = filtered_df[filtered_df["Race"].isin(selected_race)]
    avg_salary = filtered_job_gender["Salary"].mean()
    group_avg = filtered_df.groupby("Job Title")["Salary"].mean().reset_index()
    filtered_group_avg = group_avg[group_avg['Job Title'].isin(filtered_race['Job Title'])]
    top_salary = group_avg.loc[group_avg["Salary"].idxmax(), 'Salary']


#FIRST VISUALIZATION:  Salary by Gender and Job Title

with st.container():

    st.subheader("Salary Bar chart by Gender and Job Title")
    avg_chart = alt.Chart(filtered_job_gender).mark_point().encode(
        x=alt.X('Salary:Q', title='Gender'),
        y=alt.Y('Salary:Q', title='Salary'),
    )
    st.altair_chart(avg_chart, use_container_width= True)


#Top Earning Job Titles Across Races using multiple select box on what race you want to compare to


with st.container():
    
    race_visual = alt.Chart(filtered_group_avg).mark_bar().encode(
            x=alt.X('Salary:Q', title='Average Salary'),
            y=alt.Y('Job Title', title='Job  Title', sort='-x'),
            
            color="Job Title:N"  
        )
    st.altair_chart(race_visual, use_container_width= True)

with st.sidebar:
    with st.form('money'):
        st.header("Select Filter of Choosing:")
        selected_x_var = st.selectbox("x variable", filtered_df.columns)
        selected_job = st.selectbox("Job Title", filtered_df["Job Title"].unique())
        selected_gender = st.selectbox("Gender", filtered_df['Gender'].unique())

        st.form_submit_button("submit") 
        #st.header("Select Filter of Choosing:")
    filtered_job_gender = filtered_df[(filtered_df["Gender"] == selected_gender) & (filtered_df['Job Title'] == selected_job)]
    filtered_job = filtered_df[filtered_df["Job Title"] == selected_job]
    avg_salary = filtered_job_gender["Salary"].mean()
        

#All Job Title Bar Chart

with st.container():
    
    st.subheader('Job Titles')
    st.write("This Bar Chart shows the different Job titles that can be found in the data set, the highlighted bar shows the most job in the data set")
    jobtitle_count = filtered_df["Job Title"].value_counts().reset_index()
    jobtitle_count.columns = ['Job Title', 'Count']
    popular_job = jobtitle_count.loc[jobtitle_count["Count"].idxmax(), 'Job Title']

    fig = alt.Chart(jobtitle_count).mark_bar().encode(
        x='Job Title:O',
        y="Count:Q",
        # The highlight will be set on the result of a conditional statement
        color=alt.condition(
            alt.datum["Job Title"] == popular_job,
            alt.value('red'),    
            alt.value('steelblue')   
        )
    )

    st.altair_chart(fig, use_container_width= True)

#Age filter Scatter Plot

with st.container():

    st.subheader('Age scatter plot (With Filter)')
    st.write("This scatter plot shows the different ages accroding to the filters")
    chart = alt.Chart(filtered_job).mark_point().encode(
        x=alt.X('Age', title='Age'),
        y=alt.Y(selected_x_var, title=selected_x_var),
    ).properties(width=500)

    st.altair_chart(chart)

      
#Gender Male Female Pie Chart

with st.container():

    st.subheader("Gender Pie Chart")
    st.write("This Pie chart shows the percentage of Male and Female of the selected Job Title")
    filtered_gender_count = filtered_job["Gender"].value_counts().reset_index()
    #gender_count = filtered_df["Gender"].value_counts().reset_index()
    fig = px.pie(filtered_gender_count , values='Gender', names= filtered_df["Gender"].unique(), title='Male Female Percentage')
    st.plotly_chart(fig)


with st.container():

    average_salary = filtered_df.groupby('Job Title')['Salary'].mean().reset_index()
    average_salary = average_salary.sort_values(by = 'Salary',ascending = False)
    top_10 = average_salary.head(10)
    avg_chart = alt.Chart(top_10).mark_bar().encode(
        x=alt.X('Job Title:O', title='Job Title',sort='-y'),
        y=alt.Y('Salary', title='Job Average Salary'),
        color=alt.value('blue')
    )
    st.altair_chart(avg_chart, use_container_width= True)


with st.container():

    st.subheader('Salary scatter plot (Gender Filter)')
    st.write("This scatter plot shows the different ages accroding to the filters")
    chart = alt.Chart(filtered_job).mark_point().encode(
        x=alt.X('Age', title='Age'),
        y=alt.Y(selected_x_var, title=selected_x_var),
    ).properties(width=500)

    st.altair_chart(chart)

with st.container():

    st.subheader("Salary Bar chart by Gender and Job Title")
    avg_chart = alt.Chart(filtered_job_gender).mark_point().encode(
        x=alt.X('Salary:Q', title='Salary'),
        y=alt.Y('Salary:Q', title='Salary'),
    ).properties(width=500)
    st.altair_chart(avg_chart)


    
#Average Salary by Gender and Job Title:
    

#Salary Distribution by Education Level and Country:
#Top Earning Job Titles Across Races:
#Gender Pay Gap by Job Title and Country
#Salary Comparison Between Job Titles in Different Countries: 
#Salary Growth Over Years of Experience for Specific Job Titles: