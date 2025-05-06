import cv2
import numpy as np
import streamlit as st
import os
from PIL import Image
import sqlite3
import face_recognition

# Connect to SQLite database
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Create attendance table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    subjects TEXT NOT NULL,
                    date DATE NOT NULL,
                    status TEXT NOT NULL
                )''')
conn.commit()

st.title("Face Recognition Based Attendance System")

# Select multiple subjects
subjects = st.multiselect('Select Subjects', ['Subject1', 'Subject2', 'Subject3', 'Subject4'])

# Function to mark attendance
def mark_attendance(username, subjects, status):
    # Insert attendance record into the database
    cursor.execute("INSERT INTO attendance (username, subjects, date, status) VALUES (?, ?, date('now'), ?)", (username, ', '.join(subjects), status))
    conn.commit()

# Capture Video
video_capture = cv2.VideoCapture(0)

frameST = st.empty()

# Input field for the username
username = st.text_input("Enter Your Name")

# Create a button to capture photo and mark attendance
if st.button('Capture and Mark Attendance'):
    # Capture a photo
    ret, frame = video_capture.read()
    if ret:
        # Convert BGR image to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) > 0:  # If a face is detected
            if username:  # Check if username is provided
                # Mark attendance for the detected face
                mark_attendance(username, subjects, 'Present')
                st.success("Attendance marked successfully")
            else:
                st.warning("Please enter your name")
        else:
            st.warning("No face detected")

def get_attendance_data():
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    return rows
            
# Function to format and display attendance data as a table
def display_attendance_data(attendance_data):
    if not attendance_data:
        st.write("No attendance records found.")
        return
    
    # Display attendance data in a table format
    st.write("## Attendance Records")
    #st.write("<style> table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 8px;}</style>", unsafe_allow_html=True)
    #st.write("<table><tr><th>User</th><th>Status</th><th>Subjects</th><th>Date</th></tr>")
    for row in attendance_data:
        st.write(f"<tr><td>{row[1]}</td><td>{row[4]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>", unsafe_allow_html=True)
    st.write("</table>", unsafe_allow_html=True)

# Show attendance
# Show attendance
if st.button('Show Attendance'):
    attendance_data = get_attendance_data()
    display_attendance_data(attendance_data)

# Release video capture
video_capture.release()
conn.close()
