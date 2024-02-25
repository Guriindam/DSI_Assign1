import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.express as px
st.set_page_config(layout="wide")

#streamlit run c:/Users/digit/OneDrive/Desktop/DSI_Assign1/AS1_DSI_Main_22FTT1367.py

# Data Preparation
df = pd.read_csv("Salary.csv")
#st.title("Salary Across Different Demographics")
job_title_counts = df['Job Title'].value_counts()
#st.write(job_title_counts)

#Removing job columns that only have 10 or less rows
job1 = job_title_counts[job_title_counts <= 10].index

filtered_df = df[~df['Job Title'].isin(job1)]

job_title_new_count = filtered_df['Job Title'].value_counts()


st.title(":bar_chart: Salary Visualizations")
st.markdown("##")


# Filter 1

with st.sidebar:
    st.header("Select Job Title")
    selected_job_gap = st.selectbox("Select Job Title 🧑🏻‍💻", filtered_df["Job Title"].unique())

filtered_job_gap = filtered_df[filtered_df["Job Title"] == selected_job_gap]
avg_salary_male = filtered_job_gap[filtered_job_gap['Gender'] == 'Male']['Salary'].mean()
avg_salary_female = filtered_job_gap[filtered_job_gap['Gender'] == 'Female']['Salary'].mean()
salary_gap = avg_salary_male - avg_salary_female

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.write(f"Average Salary for Male: ${avg_salary_male:.2f}")
with middle_column:
    st.write(f"Average Salary for Female: ${avg_salary_female:.2f}")
with right_column:
    st.write(f"Salary Gap: ${salary_gap:.2f}")

st.markdown("---")

#First Visualization Salary Gap between Male and Female for Selected Job
with st.container():
    st.subheader("Salary Gap between Male and Female for Selected Job")
    gap_data = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Average Salary': [avg_salary_male, avg_salary_female]
    })

    gap_chart = alt.Chart(gap_data).mark_bar().encode(
        x='Gender',
        y='Average Salary',
        color=alt.Color('Gender').scale(scheme="set2")
    ).properties(
        title=f"Salary Gap between Male and Female for {selected_job_gap}"
    )

    st.altair_chart(gap_chart, use_container_width=True)


# Filter 2

with st.sidebar:
    with st.form('Filter 2'):
            st.header("Select Filter of Choosing:")
            selected_job = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())
            selected_gender = st.selectbox("Select Gender", filtered_df['Gender'].unique())
            st.form_submit_button("submit") 
            
    filtered_job = filtered_df[filtered_df["Job Title"] == selected_job]
    filtered_job_gender = filtered_df[(filtered_df["Gender"] == selected_gender) & (filtered_df['Job Title'] == selected_job)]
    avg_salary = filtered_job_gender["Salary"].mean()

#SECOND VISUALIZATION:  Salary by Gender and Job Title

with st.container():
    st.subheader("Salary Scatter Plot by Gender and Job Title")
    avg_chart = alt.Chart(filtered_job_gender).mark_point().encode(
        x=alt.X('Salary:Q', title='Salary'),
        y=alt.Y('Salary:Q', title='Salary'),
    )
    st.altair_chart(avg_chart, use_container_width= True)


# Filter 3

with st.sidebar:
    with st.form('Filters 3'):
        selected_race = st.multiselect("Select Race :smiling_imp:", filtered_df["Race"].unique())
        selected_job_bar = st.selectbox("Select Job Title :smiling_imp:", filtered_df["Job Title"].unique())
        st.form_submit_button("submit") 
        
    filtered_job_bar = filtered_df[filtered_df["Job Title"] == selected_job_bar]
    filtered_race = filtered_df[filtered_df["Race"].isin(selected_race)]
    filtered_job_race = filtered_df[(filtered_df["Job Title"] == selected_job_bar) & (filtered_df["Race"].isin(selected_race))]
    avg_salary_by_race = filtered_job_race.groupby("Race")["Salary"].mean().reset_index()


# Filter 4

with st.sidebar:
    selected_race_pie = st.multiselect("Select Race 🤖", filtered_df["Race"].unique())
    selected_job_pie = st.selectbox("Select Job Title 🤖", filtered_df["Job Title"].unique())
filtered_job_pie = filtered_df[filtered_df["Job Title"] == selected_job_pie]
filtered_race_pie = filtered_df[filtered_df["Race"].isin(selected_race_pie)]

filtered_race_job_pie = filtered_job_pie[filtered_job_pie["Race"].isin(selected_race_pie)]
#THIRD VISUALIZATION:  Average Salary of Selected Job Title for Selected Race
#FOURTH VISUALIZATION:  Percentage of Race for Selected Job Title

with st.container():

     col1, col2 = st.columns([0.5, 0.5])
 

     with col1:
        st.subheader("Average Salary of Selected Job Title for Selected Race")
        avg_salary_race_chart = alt.Chart(avg_salary_by_race).mark_bar().encode(
            x=alt.X('Race:N', title='Race'),
            y=alt.Y('Salary:Q', title='Average Salary'),
            color= alt.Color('Race').scale(scheme="dark2"),
            tooltip=[alt.Tooltip('Race:N', title='Race'), alt.Tooltip('Salary:Q', title='Average Salary', format='$,.2f')]
        ).properties(
            width=600,
            height=400
        ).configure_axisX(labelAngle=-45)

        st.altair_chart(avg_salary_race_chart, use_container_width=True)

     with col2:
        st.subheader("Percentage of Race for Selected Job Title")
        race_percentage = filtered_race_job_pie["Race"].value_counts() * 100
        fig_pie = px.pie(
            values=race_percentage.values,
            names=race_percentage.index,
            color_discrete_sequence=px.colors.sequential.Cividis,
            title=f"Percentage of Race for {selected_job_pie}",
            labels={'label':'Race', 'values':'Percentage'}
        )
        st.plotly_chart(fig_pie, use_container_width=False)


# Filter 5

with st.sidebar:
    with st.form('Filter 4'):
        st.header("Select Filter of Choosing:")
        selected_country = st.multiselect("Select Countries", filtered_df["Country"].unique())
        selected_job_2 = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())
        st.form_submit_button("submit") 
        
    
    selected_country_job = filtered_df[filtered_df["Country"].isin(selected_country) & (filtered_df["Job Title"] == selected_job_2)]

avg_salary_by_job_country = selected_country_job.groupby(["Job Title", "Country"])["Salary"].mean().reset_index()


#FIFTH VISUALIZATION:  Salary Comparison Between Job Titles in Different Countries

with st.container():
    st.subheader("Salary Comparison Between Job Titles in Different Countries")
    job_country_bar = px.bar(
        avg_salary_by_job_country,
        x="Country",
        y="Salary",
        color="Country",
        color_discrete_sequence =px.colors.qualitative.Plotly,
        title=f"Average Salary Comparison for {selected_job_2} in Different Countries",
        labels={'Salary':'Average Salary', 'Country':'Country'}
    )
    job_country_bar.update_layout(xaxis_title="Country", yaxis_title="Average Salary")
    st.plotly_chart(job_country_bar, use_container_width=True)



# Filter 6

with st.sidebar:
    st.header("Select Job")
    selected_job_title = st.selectbox("Select Job Title", filtered_df["Job Title"].unique())

selectedjob_3 = filtered_df[filtered_df["Job Title"] == selected_job_title]
avg_salary_by_experience = selectedjob_3.groupby(["Years of Experience", "Job Title"])["Salary"].mean().reset_index()


#SIXTH VISUALIZATION:  Salary Comparison Between Job Titles in Different Countries

with st.container():
    st.subheader("Salary Growth Over Years of Experience for Select Job Title")
job_yoe_line = px.line(
    avg_salary_by_experience,
    x="Years of Experience",
    y="Salary",
    title=f"Salary Growth Over Years of Experience for {selected_job_title}"
)

job_yoe_line.update_layout(xaxis_title="Years of Experience", yaxis_title="Average Salary")

st.plotly_chart(job_yoe_line, use_container_width=True)




# Filter 7

with st.sidebar:
    st.header("Select Educatuion level and Country")
    selected_education = st.selectbox("Select Education Level", df["Education Level"].unique())
    selected_countries = st.multiselect("Select Countries", df["Country"].unique())

filtered_edu = filtered_df[(filtered_df["Education Level"] == selected_education) & (filtered_df["Country"].isin(selected_countries))]
avg_salary_by_education_country = filtered_edu.groupby(["Education Level", "Country"])["Salary"].mean().reset_index()


#SEVENTH VISUALIZATION: Salary Growth Over Years of Experience for Select Job Title
with st.container():
    st.subheader("Average Salary By Selected Education Level in Different Country")
    
fig = px.bar(
    avg_salary_by_education_country,
    x="Country",
    y="Salary",
    color="Country",
    color_discrete_sequence =px.colors.qualitative.Plotly,
    title=f"Salary Distribution by Education Level ({selected_education}) and Countries ({', '.join(selected_countries)})",
    labels={'Salary':'Average Salary', 'Country':'Country'}
)

fig.update_layout(xaxis_title="Country", yaxis_title="Average Salary")

st.plotly_chart(fig, use_container_width=True)