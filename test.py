import pickle
import pickletools
import pickle
import pickletools


import joblib
from sklearn import __version__ as sklearn_version


# Load the pickled model
with open(r"C:\Users\shubh\Downloads\random_forest1.pkl", "rb") as f:
    loaded_object = pickle.load(f)

print(type(loaded_object))
