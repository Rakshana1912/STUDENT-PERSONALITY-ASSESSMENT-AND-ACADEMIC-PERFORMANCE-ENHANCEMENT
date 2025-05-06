import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import pickle

# Directory where images are stored
image_dir = 'images'
known_face_encodings = []
known_face_names = []

# Load previously saved encodings if any
if os.path.exists('encodings.pkl'):
    with open('encodings.pkl', 'rb') as file:
        known_face_encodings, known_face_names = pickle.load(file)

def mark_attendance(name, subjects, status):
    attendance = pd.read_csv('attendance.csv')

    if name not in attendance['Name'].values:
        new_idx = len(attendance)
        attendance.loc[new_idx, 'Name'] = name
        for subject in subjects:
            attendance.loc[new_idx, subject] = status
    else:
        for subject in subjects:
            attendance.loc[attendance['Name'] == name, subject] = status

    attendance.to_csv('attendance.csv', index=False)

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Read video frame
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Mark attendance as present
           
            print("foundddddddddddddddddddddddddddd")
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Mark attendance as absent
        mark_attendance('Unknown', ['Subject1', 'Subject2'], 'Absent')
        break

# Release video capture
video_capture.release()
cv2.destroyAllWindows()
mark_attendance(name, ['Subject1', 'Subject2'], 'Present')