import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.express as px
st.set_page_config(layout="wide")

df = pd.read_csv("Salary.csv")
#st.title("Salary Across Different Demographics")
job_title_counts = df['Job Title'].value_counts()
#st.write(job_title_counts)

#Removing job columns that only have 10 or less rows
job1 = job_title_counts[job_title_counts <= 10].index
# The ~ acts as a boolean button
filtered_df = df[~df['Job Title'].isin(job1)]

job_title_new_count = filtered_df['Job Title'].value_counts()

#st.write(job_title_new_count)

#Filters
with st.sidebar:
    with st.form('Filters'):
        st.header("Select Filter of Choosing:")
        selected_job = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())
        selected_gender = st.selectbox("Select Gender", filtered_df['Gender'].unique())
        st.form_submit_button("submit") 

with st.sidebar:
        selected_race = st.multiselect("Select Race :smiling_imp:", filtered_df["Race"].unique())
        
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




    # Average Salary by Job Title for Selected Race
    st.subheader("Average Salary by Job Title for Selected Race")
    race_visual = alt.Chart(filtered_group_avg).mark_bar().encode(
        x=alt.X('Salary:Q', title='Average Salary'),
        y=alt.Y('Job Title:N', title='Job Title', sort='-x'),
        color=alt.Color('Job Title:N', legend=None)
    )
    st.altair_chart(race_visual, use_container_width=True)



with st.container():

     col1, col2 = st.columns([0.5, 0.5])
 

     with col1:
        st.subheader("Average Salary of Selected Job Title for Selected Race")
        filtered_job_race = filtered_df[(filtered_df["Job Title"] == selected_job) & (filtered_df["Race"].isin(selected_race))]
        avg_salary_by_race = filtered_job_race.groupby("Race")["Salary"].mean().reset_index()

        avg_salary_race_chart = alt.Chart(avg_salary_by_race).mark_bar().encode(
            x=alt.X('Race:N', title='Race'),
            y=alt.Y('Salary:Q', title='Average Salary'),
            tooltip=[alt.Tooltip('Race:N', title='Race'), alt.Tooltip('Salary:Q', title='Average Salary', format='$,.2f')]
        ).properties(
            width=600,
            height=400
        ).configure_axisX(labelAngle=-45)

        st.altair_chart(avg_salary_race_chart, use_container_width=True)

     with col2:
        st.subheader("Percentage of Race for Selected Job Title")
        race_percentage = filtered_race["Race"].value_counts(normalize=True) * 100
        fig_pie = px.pie(
            values=race_percentage.values,
            names=race_percentage.index,
            title=f"Percentage of Race for {selected_job}",
            labels={'label':'Race', 'values':'Percentage'}
        )
        fig_pie.update_layout(
        autosize=False,
        width=500,
        height=450
        )
        st.plotly_chart(fig_pie, use_container_width=False)

        


with st.sidebar:
    with st.form('Filter 2'):
        st.header("Select Filter of Choosing:")
        selected_country = st.multiselect("Select Countries", filtered_df["Country"].unique())
        selected_job_2 = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())
        st.form_submit_button("submit") 
        
    
    selected_country_job = filtered_df[filtered_df["Country"].isin(selected_country) & (filtered_df["Job Title"] == selected_job_2)]

# Group by job title and country to calculate the average salary
avg_salary_by_job_country = selected_country_job.groupby(["Job Title", "Country"])["Salary"].mean().reset_index()

# Bar chart for salary comparison between job titles in different countries
with st.container():
    st.subheader("Salary Comparison Between Job Titles in Different Countries")
    fig = px.bar(
        avg_salary_by_job_country,
        x="Country",
        y="Salary",
        color="Country",
        title=f"Average Salary Comparison for {selected_job_2} in Different Countries",
        labels={'Salary':'Average Salary', 'Country':'Country'}
    )
    fig.update_layout(xaxis_title="Country", yaxis_title="Average Salary")
    st.plotly_chart(fig, use_container_width=True)


with st.sidebar:
    st.header("Select Job")
    selected_job_title = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())

selectedjob_3 = filtered_df[filtered_df["Job Title"] == selected_job_title]
avg_salary_by_experience = selectedjob_3.groupby(["Years of Experience", "Job Title"])["Salary"].mean().reset_index()

# Plot salary growth over years of experience for selected job titles
jobByYearOfExperience = px.line(
    avg_salary_by_experience,
    x="Years of Experience",
    y="Salary",
    title=f"Salary Growth Over Years of Experience for {selected_job_title}"
)

# Update figure layout
fig.update_layout(xaxis_title="Years of Experience", yaxis_title="Average Salary")

st.plotly_chart(jobByYearOfExperience, use_container_width=True)

with st.sidebar:
    st.header("Filters")
    selected_education = st.selectbox("Select Education Level", df["Education Level"].unique())
    selected_countries = st.multiselect("Select Countries", df["Country"].unique())


filtered_edu = filtered_df[(filtered_df["Education Level"] == selected_education) & (filtered_df["Country"].isin(selected_countries))]

# Group by education level and country to calculate average salary
avg_salary_by_education_country = filtered_edu.groupby(["Education Level", "Country"])["Salary"].mean().reset_index()

# Create plot
fig = px.bar(
    avg_salary_by_education_country,
    x="Country",
    y="Salary",
    color="Country",
    title=f"Salary Distribution by Education Level ({selected_education}) and Countries ({', '.join(selected_countries)})",
    labels={'Salary':'Average Salary', 'Country':'Country'}
)

# Update layout
fig.update_layout(xaxis_title="Country", yaxis_title="Average Salary")

# Show plot
st.plotly_chart(fig, use_container_width=True)