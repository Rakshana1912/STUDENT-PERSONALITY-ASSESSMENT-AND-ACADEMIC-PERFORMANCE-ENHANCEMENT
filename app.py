import streamlit as st
from streamlit import session_state
import sqlite3
from PIL import Image
from PIL import Image, ImageDraw
import json
import base64
import os
import face_recognition
# Function to extract face encodings
def extract_face_encodings(image_file):
    img = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(img)
    if len(face_encodings) == 0:
        return None
    return face_encodings[0]
# Modify the add_user function to include face encodings
def add_user(username, password, contact, email, profile_image):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    # Extract face encodings
    face_encodings = extract_face_encodings(profile_image)
    
    if face_encodings is not None:
        # Convert face encodings to string for storage
        face_encodings_str = json.dumps(face_encodings.tolist())
        
        # Insert user information into the database
        c.execute('INSERT INTO users(username, password, contact, email, face_encodings) VALUES (?,?,?,?,?)',
                  (username, password, contact, email, face_encodings_str))
        conn.commit()
        st.success("User added successfully")
    else:
        st.warning("No face detected in the uploaded image")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
# add_bg_from_local('bg.jpg')
from PIL import Image, ImageDraw

def crop_to_circle(image):
    # Create a circular mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)

    # Apply the circular mask to the image
    result = Image.new("RGBA", image.size)
    result.paste(image, (0, 0), mask)

    return result



def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, contact TEXT, email TEXT, face_encodings TEXT)')
    conn.commit()


def get_user(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    user_info = c.execute('SELECT * FROM users WHERE username =?', (username,))
    for row in user_info:
        return row
    return None
# Function to navigate to different pages based on button clicks
def navigate_to_page(page):
    session_state.page = page

def main():
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu, key='menu_select')

    if choice == "Home":
        st.header("STUDENT TRACKER")
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        with columns[1]:
            st.image("home.png",width=300)
        st.markdown("""
        ## Features

### 1. Predictive Analysis
Leverage the power of machine learning to foresee future academic trends. This feature uses past data and current variables to predict student performance, academic outcomes, and more. It's a strategic tool that supports educators in creating a better learning environment by anticipating potential challenges and opportunities.

### 2. Performance Analysis on the Basis of Regular Inputs
Consistently monitor student progress with this interactive performance analysis tool. By collecting regular inputs, it provides timely, in-depth insights into each student's strengths and weaknesses, thereby enabling a more targeted and individualized learning approach.

### 3. Risk Subjects Page
The Risk Subjects Page is a dedicated interface for identifying and managing potential academic risks. This page displays subjects where students may be struggling, providing educators with the necessary data to implement interventions or additional support as necessary.

### 4. Course Recommendation
Our platform takes a personalized approach to education. By understanding each student's interests, strengths, and academic history, it suggests the most suitable courses for them. This way, students can pursue learning pathways that resonate with their personal and professional goals.

### 5. Academic Performance History Based on Past Data
This feature offers a comprehensive view of a student's academic journey. By analyzing historical data, it depicts trends in the student's performance, illustrating their growth, areas of improvement, and ongoing challenges. This valuable resource supports both students and educators in decision-making processes.

### 6. Attendance Record
Ensure accurate and seamless tracking of student attendance with our Attendance Record feature. It's a straightforward, user-friendly tool that not only records attendance but also offers insights into attendance patterns and their correlation with academic performance.

### 7. Student Quality Analysis
This robust feature provides a holistic view of student potential and capacity. It evaluates not just academic performance but also other factors like engagement, extracurricular activities, and behavioral tendencies to measure student quality.

### 8. Summary of DOX Page
The Summary of DOX Page consolidates all essential documents, notes, and relevant educational resources in one place for easy access. It's an efficient way to keep track of crucial information and enhance study efficiency.

### 9. Question Generation for Practice
With this feature, students can generate custom practice questions based on their learning needs. It's a flexible, adaptive tool that supports continuous learning and revision, helping students gain mastery over their subjects.

### 10. Exam Strategy Maker Based on Inputs
This feature empowers students to approach their exams strategically. By analyzing individual learning styles, subject knowledge, and past performance, it helps students create an effective exam plan that maximizes their chances of success.

### 11. Progress Tracking
Keep your academic journey on track with our Progress Tracking feature. It provides a visual representation of your learning progress, helping you understand where you stand, what you've achieved, and what your next learning goals should be. This feature helps maintain focus and drive towards success.

        """)
    elif choice == "Login":
        st.header("Academic Tracker")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            create_users_table()
            user_info = get_user(username)
            if user_info and user_info[1] == password:
                st.success("Logged In as {}".format(username))
                col1, col2, col3 = st.columns(3)
                columns = [col1, col2, col3]
                with columns[1]:
                    st.image("profile_circle.png", width=300, output_format='PNG')
                # Profile photo upload
                uploaded_file = st.file_uploader("Choose a profile picture...", type=["jpg", "png","jpeg"], key='profile_upload')
                if uploaded_file is not None:
                    img = Image.open(uploaded_file)
                    img = crop_to_circle(img)
                    img.save("profile_circle.png", "PNG")
                    
                
                # User information display
                st.markdown('<p style="text-align: center;">Username: {}</p>'.format(user_info[0]), unsafe_allow_html=True)
                #st.markdown('<p style="text-align: center;">Contact: {}</p>'.format(user_info[2]), unsafe_allow_html=True)
                #st.markdown('<p style="text-align: center;">Email: {}</p>'.format(user_info[3]), unsafe_allow_html=True)

                # List of image URLs and texts for the boxes
                box_images = ['http://placehold.it/350x150', 'http://placehold.it/350x150', 'http://placehold.it/350x150', 'http://placehold.it/350x150', 'http://placehold.it/350x150', 'http://placehold.it/350x150']
                box_texts = ['Attendence Monitor system', 'Student Analysis System', 'Personality Predictor', 'Course Recommender', 'Question Generator', 'Exam Strategy Maker']

                # Creating 6 boxes with different images and texts
                col1, col2, col3 = st.columns(3)
                columns = [col1, col2, col3]
                ls=[]
                for i in range(6):
                    with columns[i % 3]:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(to right, #ff7e5f, #feb47b);
                            padding: 10px;
                            border-radius: 10px;
                            box-shadow: 10px 10px 5px grey;
                            transition: transform .2s;
                            margin-bottom: 30px;
                        " class="hoverable">
                            <h3 style="text-align: center;color:black">{box_texts[i]}</h3>
                           
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("""
                        <style>
                        .hoverable:hover {
                            transform: scale(1.02);
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        x=st.button(f"View {i+1}")
                        ls.append(x)
                if ls[0]:
                    os.system("streamlit run attendance.py")
                if ls[1]:
                    os.system("streamlit run analysis.py")
                if ls[2]:
                    os.system("streamlit run ./student_personality_prediction/app.py")
                if ls[3]:
                    os.system("streamlit run recom.py")
                if ls[4]:
                    os.system("streamlit run dox.py")
                if ls[5]:
                    os.system("streamlit run stratergy.py")

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        contact = st.text_input("Contact")
        email = st.text_input("Email")
        profile_image = st.file_uploader("Upload Profile Picture...", type=["jpg", "png", "jpeg"])

        if st.button("Signup"):
            create_users_table()
            if profile_image is not None:
                add_user(new_user, new_password, contact, email, profile_image)
            else:
                st.warning("Please upload a profile picture")
            st.info("Go to Login Menu to login")

if __name__ == "__main__":
    main()



