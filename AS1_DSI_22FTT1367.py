
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



# Age,Gender,
# Education Level,Job Title,
# Years of Experience,Salary,
# Country,Race,
# Senior,Education Level,Job Title,
# Gender,Education