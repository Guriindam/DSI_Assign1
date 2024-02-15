
import pandas as pd
import numpy as np 
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.express as px



df = pd.read_csv("Salary.csv")
st.title("Salary Across Different Demographics")

with st.sidebar:
    with st.form('money'):
        st.header("Select Filter of Choosing:")
        selected_x_var = st.selectbox("x variable", df.columns)
        selected_y_var = st.selectbox("y variable", df["Job Title"].unique())
        st.form_submit_button("submit") 
        #st.header("Select Filter of Choosing:")
    filtered_job = df[df["Job Title"] == selected_y_var]
        

#All Job Title Bar Chart

with st.container():
    
    st.subheader('Job Titles')
    st.write("This Bar Chart shows the different Job titles that can be found in the data set, the highlighted bar shows the most job in the data set")
    jobtitle_count = df["Job Title"].value_counts().reset_index()
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
    #gender_count = df["Gender"].value_counts().reset_index()
    fig = px.pie(filtered_gender_count , values='Gender', names= df["Gender"].unique(), title='Male Female Percentage')
    st.plotly_chart(fig)


with st.container():

    average_salary = df.groupby('Job Title')['Salary'].mean().reset_index()
    average_salary = average_salary.sort_values(by = 'Salary',ascending = False)
    top_10 = average_salary.head(10)
    avg_chart = alt.Chart(top_10).mark_bar().encode(
        x=alt.X('Job Title:O', title='Job Title',sort='-y'),
        y=alt.Y('Salary', title='Job Average Salary'),
        color=alt.value('blue')
    )
    st.altair_chart(avg_chart, use_container_width= True)


#Average salary for selected
#Fix the first visualization                                                                                                                                            

# do visualization not based on different column, do based on the inside



with st.container():

    st.subheader('Salary scatter plot (Gender Filter)')
    st.write("This scatter plot shows the different ages accroding to the filters")
    chart = alt.Chart(filtered_job).mark_point().encode(
        x=alt.X('Age', title='Age'),
        y=alt.Y(selected_x_var, title=selected_x_var),
    ).properties(width=500)

    st.altair_chart(chart)

    #with st.form('education filter'):
        #st.write("Filter by Education Level")
        #selected_level = st.selectbox('Education Level', df['Education Level'].unique)
        #st.form_submit_button("submit") 

    #filtered_level = filtered_job[filtered_job['Education'] == selected_level]


    #with st.container():
        #st.subheader('Salary and Years Of Experience')
        #fig3 = alt.Chart(filtered_job).mark_circle().encode(
            #x=alt.X('Education', title='Education Level'),
            #y=alt.Y('Salary', title='Salary'),
            #color='Gender'
        #).properties(width=500)
        
    #st.altair_chart(fig3)

