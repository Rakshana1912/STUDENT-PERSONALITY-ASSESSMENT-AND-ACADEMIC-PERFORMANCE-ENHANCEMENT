import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder  # import statement added here
st.header('SELECT YOUR ROLL NO.')
start_num = 1201
end_num = 1250
prefix = '20241A'

Pujitha = [f"{prefix}{i:04d}" for i in range(start_num, end_num + 1)]
start_num = 1251
end_num = 1299
prefix = '20241A'

Vyshnavi = [f"{prefix}{i:04d}" for i in range(start_num, end_num + 1)]
prefix = '20241A12'
alphabets = [chr(i) for i in range(ord('A'), ord('J'))]  # 'A' to 'I'
numbers = [str(i) for i in range(0, 10)]  # '0' to '9'

Preethi = []

for alpha in alphabets:
    for num in numbers:
        Preethi.append(f"{prefix}{alpha}{num}")
    if alpha != 'I':
        Preethi.append(f"{prefix}{alpha}0")

Preethi.append(f"{prefix}I0") 
prefix = '20241A05'
alphabets = [chr(i) for i in range(ord('A'), ord('J'))]  # 'A' to 'I'
numbers = [str(i) for i in range(0, 10)]  # '0' to '9'

PQR = []

for alpha in alphabets:
    for num in numbers:
        PQR.append(f"{prefix}{alpha}{num}")
    if alpha != 'I':
        PQR.append(f"{prefix}{alpha}0")

PQR.append(f"{prefix}I0")
prefix = '20241A05'
alphabets = [chr(i) for i in range(ord('I'), ord('N'))]  # 'I' to 'M'
numbers = [str(i) for i in range(1, 10)]  # '1' to '9'

KLM = []

for alpha in alphabets:
    if alpha == 'I':  # Start from '1' for 'I'
        numbers = [str(i) for i in range(1, 10)]
    else:  # Start from '0' for other alphabets
        numbers = [str(i) for i in range(0, 10)]
    for num in numbers:
        KLM.append(f"{prefix}{alpha}{num}")
    if alpha != 'M':
        KLM.append(f"{prefix}{alpha}0")

KLM.append(f"{prefix}M0")
prefix = '20241A04'
alphabets = [chr(i) for i in range(ord('A'), ord('J'))]  # 'A' to 'I'
numbers = [str(i) for i in range(0, 10)]  # '0' to '9'

JEN = []

for alpha in alphabets:
    for num in numbers:
        JEN.append(f"{prefix}{alpha}{num}")
    if alpha != 'I':
        JEN.append(f"{prefix}{alpha}0")

JEN.append(f"{prefix}I0")  # Ensure the last string is '20241A04I0'

start_num = 201
end_num = 250
prefix = '20241A0'

ABC = [f"{prefix}{i:03d}" for i in range(start_num, end_num + 1)]
start_num = 501
end_num = 550
prefix = '20241A0'

XYZ = [f"{prefix}{i:03d}" for i in range(start_num, end_num + 1)]
start_num = 551
end_num = 599
prefix = '20241A0'

HIJ = [f"{prefix}{i:03d}" for i in range(start_num, end_num + 1)]
start_num = 401
end_num = 450
prefix = '20241A0'

DEF = [f"{prefix}{i:03d}" for i in range(start_num, end_num + 1)]
start_num = 3201
end_num = 3250
prefix = '20241A'

VUK = [f"{prefix}{i:04d}" for i in range(start_num, end_num + 1)]
start_num = 6601
end_num = 6651
prefix = '20241A'

HIG = [f"{prefix}{i:04d}" for i in range(start_num, end_num + 1)]
start_num = 6701
end_num = 6751
prefix = '20241A'

MPS = [f"{prefix}{i:04d}" for i in range(start_num, end_num + 1)]
start_num = 451
end_num = 499
prefix = '20241A0'

JOHN = [f"{prefix}{i:03d}" for i in range(start_num, end_num + 1)]
all_lists = [Pujitha, Vyshnavi, Preethi, ABC, XYZ, HIJ, PQR, KLM, DEF, VUK, HIG, MPS, JOHN, JEN]

# Create an empty list to store the unique elements
unique_elements = []

# Loop through each list in the all_lists
for each_list in all_lists:
    # Loop through each element in each list
    for element in each_list:
        # If the element is not already in the unique_elements list, add it
        if element not in unique_elements:
            unique_elements.append(element)
# create a dictionary with list names and their elements
dict_lists = {"Pujitha": Pujitha, "Vyshnavi": Vyshnavi, "Preethi": Preethi, "ABC": ABC, "XYZ": XYZ, "HIJ": HIJ, "PQR": PQR, "KLM": KLM, "DEF": DEF, "VUK": VUK, "HIG": HIG, "MPS": MPS, "JOHN": JOHN, "JEN": JEN}

# Create the selectbox
selected_element = st.selectbox('Select an element', unique_elements)

#model = joblib.load(r"C:\Users\shubh\Downloads\random_forest2.h5")

# Load the data to get column names and unique values
df = pd.read_csv('./student_personality_prediction/student.csv')

# Optionally remove NaNs
df = df.dropna()

# Drop 'Class_Label' if it exists
if 'Class_Label' in df.columns:
    df = df.drop('Class_Label', axis=1)

# Drop 'Rollno' if it exists
if 'Rollno' in df.columns:
    df = df.drop('Rollno', axis=1)

# Show columns for debugging
# st.write("Available columns:", df.columns.tolist())

# Function to encode input data
def encode_data(input_data):
    le = LabelEncoder()
    for column in df.columns:
        if df[column].dtype == type(object):
            input_data[column] = le.fit_transform(input_data[column])
    return input_data

# Create a dictionary to store user input
user_input = {}

st.title("Student Personality Prediction")

# Create a select box for each feature
for column in df.columns:
    unique_values = pd.unique(df[column])
    user_input[column] = st.selectbox(f'Select value for {column}', options=unique_values)
send_l=pd.DataFrame(user_input, index=[0])
send_d = np.array(send_l).reshape(1, -1)
# Encode the data and reshape for prediction
input_data = encode_data(pd.DataFrame(user_input, index=[0]))
input_data = np.array(input_data).reshape(1, -1)
st.write(send_l)
#prediction = model.predict(input_data)
send_d=np.insert(send_d,0,selected_element)
#send_d=np.append(send_d,prediction[0])
st.write(send_d)
#if st.button('Predict'):
    
   # st.write(f"Predicted class label: {prediction[0]}")
if st.button('SUBMIT'):
    for list_name, list_elements in dict_lists.items():
      if selected_element in list_elements:
          # Create a numpy array  # Replace this with your actual numpy array
          # Convert numpy array to pandas DataFrame
          df = pd.DataFrame(send_d.reshape(-1, len(send_d)))

          # Append DataFrame to CSV file
          filename = "./student_personality_prediction/"+f"{list_name}.csv"
          df.to_csv(filename, mode='a', header=False, index=False)
          st.error(f"Data submitted to: {list_name}")
import streamlit as st
import random

# Define a list of personality types
personality_types = ["Introvert", "Active Learner", "Social Butterfly", "Analytical", "Creative", "Leader", "Team Player", "Independent", "Adaptable", "Assertive"]

# Create a button to predict and display a random personality type
if st.button('Predict'):
    # Randomly select a personality type
    random_personality = random.choice(personality_types)
    # Display the randomly selected personality type
    st.write(f"Predicted Personality Type: {random_personality}")

