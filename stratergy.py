import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Mock dataframe for each subject
def create_dataframe(subject):
    df = pd.DataFrame({
        'Topics': ['Topic A', 'Topic B', 'Topic C', 'Topic D', 'Topic E'],
        'Score': np.random.randint(50, 100, 5),
        'Time': np.random.uniform(1.5, 3, 5),
        'Importance': np.random.choice(['High', 'Medium', 'Low'], 5)
    })
    df['Subject'] = subject
    return df

# Create a dataframe for each subject
subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Subject 6']
dfs = {subject: create_dataframe(subject) for subject in subjects}

st.title('Exam Strategy Maker')

# Input section
strategy_preferences = st.text_input("Enter your strategy preferences:", "")
study_hours_per_week = st.slider('How many hours per week do you plan to study?', min_value=0, max_value=50)
weeks_until_exam = st.slider('How many weeks until the exam?', min_value=1, max_value=52)

# Analysis section
cols = st.columns(3)

average_scores = {}

for i, subject in enumerate(subjects):
    df = dfs[subject]

    average_scores[subject] = df['Score'].mean()

    fig, ax = plt.subplots()
    ax.bar(df['Topics'], df['Score'])
    ax.set_title(f'Scores for {subject}')
    ax.set_xlabel('Topics')
    ax.set_ylabel('Score')
    cols[i%3].pyplot(fig)

    fig, ax = plt.subplots()
    ax.pie(df['Importance'].value_counts(), labels=df['Importance'].value_counts().index, autopct='%1.1f%%')
    ax.set_title(f'Importance of topics for {subject}')
    cols[i%3].pyplot(fig)

    with st.expander(f'{subject} DataFrame'):
        st.write(df)

# Risk subject section
risk_subject = min(average_scores, key=average_scores.get)
st.write(f'The predicted risk subject based on average scores is: {risk_subject}')
