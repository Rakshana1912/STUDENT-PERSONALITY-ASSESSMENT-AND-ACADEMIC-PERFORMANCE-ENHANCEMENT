import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Define the path to the CSV file
csv_file = 'student_data.csv'

# Check if the file exists
if not os.path.isfile(csv_file):
    # Create a new dataframe with the required columns
    df = pd.DataFrame(columns=[
        "Grade/Class", "Subject", "Attendance", "Test Scores", "Homework Scores", 
        "Project Scores", "Participation", "Final Grade", "Parental Education", 
        "Socioeconomic Status", "Extracurricular Activities", "Special Needs", "Behavior/Conduct"
    ])

    # Write the dataframe to a new CSV file
    df.to_csv(csv_file, index=False)

# Function to write data to CSV
def write_data(data):
    df = pd.DataFrame([data], columns=list(data.keys()))
    df.to_csv(csv_file, mode='a', index=False, header=not os.path.getsize(csv_file) > 0)
    st.success("Data saved successfully!")

# Function to plot the data
def plot_data():
    try:
        df = pd.read_csv(csv_file)
        
        # Check if we have at least 2 entries for comparison
        if df.shape[0] >= 2:
            st.write("## Comparing Current Student Data with Previous Student")
            
            # Fill NaN values with 0 for numerical plotting
            df_plot = df.fillna(0)
            
            # Line plot for test, homework and project scores
            st.write("### Line Plot for Test, Homework, and Project Scores")
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df_plot[['Test Scores', 'Homework Scores', 'Project Scores']][-2:])
            plt.xticks(ticks=range(2), labels=['Previous Student', 'Current Student'])
            st.pyplot(plt.gcf())
            plt.close()

            # Pie chart for attendance and participation
            st.write("### Pie Chart for Attendance and Participation")
            
            # Check for NaN values and handle them
            latest_two_attendance = df_plot['Attendance'][-2:].values
            latest_two_participation = df_plot['Participation'][-2:].values
            
            # Create subplots
            fig, ax = plt.subplots(1, 2, figsize=(10, 5))
            
            # Only create pie charts if values are valid
            if not np.isnan(latest_two_attendance).any() and np.sum(latest_two_attendance) > 0:
                ax[0].pie(latest_two_attendance, labels=['Previous Student', 'Current Student'], autopct='%1.1f%%')
                ax[0].set_title('Attendance')
            else:
                ax[0].text(0.5, 0.5, 'Insufficient data', horizontalalignment='center', verticalalignment='center')
                ax[0].set_title('Attendance (No Data)')
            
            if not np.isnan(latest_two_participation).any() and np.sum(latest_two_participation) > 0:
                ax[1].pie(latest_two_participation, labels=['Previous Student', 'Current Student'], autopct='%1.1f%%')
                ax[1].set_title('Participation')
            else:
                ax[1].text(0.5, 0.5, 'Insufficient data', horizontalalignment='center', verticalalignment='center')
                ax[1].set_title('Participation (No Data)')
                
            st.pyplot(fig)
            plt.close()

            # Bar plot for final grade
            st.write("### Bar Plot for Final Grade")
            plt.figure(figsize=(10, 5))
            sns.barplot(x=['Previous Student', 'Current Student'], y=df_plot['Final Grade'][-2:])
            st.pyplot(plt.gcf())
            plt.close()

            # Histogram for socioeconomic status if there's enough data
            if not df['Socioeconomic Status'].isna().all():
                st.write("### Histogram for Socioeconomic Status")
                plt.figure(figsize=(10, 5))
                sns.histplot(df['Socioeconomic Status'].dropna(), kde=True)
                st.pyplot(plt.gcf())
                plt.close()

            # Scatterplot for test scores versus final grade if there's enough data
            if not df['Test Scores'].isna().all() and not df['Final Grade'].isna().all():
                st.write("### Scatterplot for Test Scores versus Final Grade")
                plt.figure(figsize=(10, 5))
                valid_data = df.dropna(subset=['Test Scores', 'Final Grade'])
                if len(valid_data) > 1:  # Ensure we have at least 2 points
                    sns.scatterplot(x=valid_data['Test Scores'], y=valid_data['Final Grade'])
                    st.pyplot(plt.gcf())
                else:
                    st.warning("Not enough non-null data for scatter plot.")
                plt.close()

            # Boxplot for attendance if there's enough data
            if not df['Attendance'].isna().all():
                st.write("### Boxplot for Attendance")
                plt.figure(figsize=(10, 5))
                sns.boxplot(y=df['Attendance'].dropna())
                st.pyplot(plt.gcf())
                plt.close()

            # Bar plot for extracurricular activities
            st.write("### Bar Plot for Extracurricular Activities")
            plt.figure(figsize=(10, 5))
            sns.barplot(x=['Previous Student', 'Current Student'], y=df_plot['Extracurricular Activities'][-2:])
            st.pyplot(plt.gcf())
            plt.close()
        else:
            st.warning("Not enough data for comparison. Please enter at least two students' data.")
    except Exception as e:
        st.error(f"Error plotting data: {str(e)}")
        st.info("Please ensure the CSV file contains valid data and try again.")

# Collect student data
st.write("# Enter Student Data")

data = {
    "Grade/Class": st.number_input('Grade/Class', value=0, min_value=0),
    "Subject": st.text_input('Subject', value=''),
    "Attendance": st.number_input('Attendance', value=0.0, min_value=0.0),
    "Test Scores": st.number_input('Test Scores', value=0.0, min_value=0.0),
    "Homework Scores": st.number_input('Homework Scores', value=0.0, min_value=0.0),
    "Project Scores": st.number_input('Project Scores', value=0.0, min_value=0.0),
    "Participation": st.number_input('Participation', value=0.0, min_value=0.0),
    "Final Grade": st.number_input('Final Grade', value=0.0, min_value=0.0),
    "Parental Education": st.number_input('Parental Education', value=0.0, min_value=0.0),
    "Socioeconomic Status": st.number_input('Socioeconomic Status', value=0.0, min_value=0.0),
    "Extracurricular Activities": st.number_input('Extracurricular Activities', value=0.0, min_value=0.0),
    "Special Needs": st.selectbox('Special Needs', options=['Yes', 'No'], index=1),
    "Behavior/Conduct": st.number_input('Behavior/Conduct', value=0.0, min_value=0.0)
}

# Convert Special Needs to numeric for storage
data["Special Needs"] = 1 if data["Special Needs"] == "Yes" else 0

if st.button('Submit'):
    write_data(data)

plot_data()