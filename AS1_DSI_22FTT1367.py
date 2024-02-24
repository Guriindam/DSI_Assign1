import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("Salary.csv")
# st.title("Salary Across Different Demographics")
job_title_counts = df['Job Title'].value_counts()

# Removing job columns that only have 10 or fewer rows
job1 = job_title_counts[job_title_counts <= 10].index
# The ~ acts as a boolean button
filtered_df = df[~df['Job Title'].isin(job1)]

# Define filters
min_age = filtered_df["Age"].min()
max_age = filtered_df["Age"].max()
age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

with st.sidebar:
    st.header("Filters")
    gender = st.selectbox('Gender', filtered_df['Gender'].unique())
    edu_level = st.selectbox('Education Level', filtered_df['Education Level'].unique())
    job_title_1 = st.selectbox('Job Title 1', filtered_df['Job Title'].unique())
    job_title_2 = st.selectbox('Job Title 2', filtered_df['Job Title'].unique())
    years_exp_range = st.slider('Years of Experience', filtered_df['Years of Experience'].min(),
                                filtered_df['Years of Experience'].max(), (filtered_df['Years of Experience'].min(), filtered_df['Years of Experience'].max()))
    salary_range = st.slider('Salary Range', filtered_df['Salary'].min(), filtered_df['Salary'].max(),
                            (filtered_df['Salary'].min(), filtered_df['Salary'].max()))
    country1 = st.selectbox('Country1', filtered_df['Country'].unique())
    selected_race_pie = st.multiselect("Select Race 🤖", filtered_df["Race"].unique())
    selected_country_pie = st.selectbox('Country2', filtered_df['Country'].unique())



filtered_country_pie = filtered_df[filtered_df["Country"] == selected_country_pie]

filtered_race_pie = filtered_df[filtered_df["Race"].isin(selected_race_pie)]

filtered_age = filtered_df[(filtered_df['Age'].between(age_range[0], age_range[1])) &
    (filtered_df['Gender'] == gender)]

filtered_edu_job = filtered_df[(filtered_df['Job Title'] == job_title_1) & (filtered_df['Education Level'] == edu_level)]

filtered_YOE_job = filtered_df[(filtered_df['Job Title'] == job_title_2) & (filtered_df['Years of Experience'].between(years_exp_range[0], years_exp_range[1]))]

filtered_salary_country = filtered_df[(filtered_df['Salary'].between(salary_range[0], salary_range[1])) & (filtered_df['Country'] == country1)]


# Age Distribution
age_chart = alt.Chart(filtered_age).mark_bar().encode(
    alt.X("Age:Q", bin=True),
    y='count()',
).properties(
    title='Age Distribution'
)

st.altair_chart(age_chart, use_container_width=True)

#Education Level Distribution
edu_level_count = filtered_edu_job['Education Level'].value_counts().reset_index()
edu_level_count.columns = ['Education Level', 'Count']
edu_level_bar = alt.Chart(edu_level_count).mark_bar().encode(
x='Education Level',
y='Count',
color='Education Level'
).properties(
title='Education Level Distribution'
)

st.altair_chart(edu_level_bar, use_container_width=True)


#  Years of Experience Distribution
exp_chart = alt.Chart(filtered_YOE_job).mark_bar().encode(
     alt.X("Years of Experience:Q", bin=True),
     y='count()',
 ).properties(
     title='Years of Experience Distribution'
 )

st.altair_chart(exp_chart, use_container_width=True)
 # Salary Distribution
salary_chart = alt.Chart(filtered_salary_country).mark_bar().encode(
     alt.X("Salary:Q", bin=True),
     y='count()',
 ).properties(
     title='Salary Distribution'
 )

st.altair_chart(salary_chart, use_container_width=True)


# Race Distribution
st.subheader("Percentage of Race for Selected Country")
race_percentage = filtered_race_pie["Race"].value_counts(normalize=True) * 100
fig_pie = px.pie(
    values=race_percentage.values,
    names=race_percentage.index,
    color_discrete_sequence=px.colors.sequential.RdBu,
    title=f"Percentage of Race for {filtered_country_pie}",
    labels={'label':'Race', 'values':'Percentage'},
)
fig_pie.update_layout(
autosize=False,
width=500,
height=450
)
st.plotly_chart(fig_pie, use_container_width=False)