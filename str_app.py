import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# Load trained model
model = load("random_forest_model.joblib")

# Initialize history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Housing Price Prediction App")
st.write("Enter housing details to estimate the price.")

# User inputs
area = st.number_input("Area (sq ft)", 200, 10000, value=1200)
bedrooms = st.selectbox("Number of Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Number of Bathrooms", [1, 2, 3])
stories = st.selectbox("Number of Stories", [1, 2, 3])
mainroad = st.selectbox("Main Road Access", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
parking = st.slider("Number of Parking Spaces", 0, 5, 1)
prefarea = st.selectbox("Preferred Area", ["yes", "no"])

# Manual feature list (must match what the model was trained on)
feature_order = [
    "area", "bedrooms", "bathrooms", "stories",
    "mainroad_yes", "guestroom_yes", "basement_yes",
    "hotwaterheating_yes", "airconditioning_yes",
    "parking", "prefarea_yes"
]

# Build input dict
input_dict = {
    "area": area,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "stories": stories,
    "mainroad_yes": 1 if mainroad == "yes" else 0,
    "guestroom_yes": 1 if guestroom == "yes" else 0,
    "basement_yes": 1 if basement == "yes" else 0,
    "hotwaterheating_yes": 1 if hotwaterheating == "yes" else 0,
    "airconditioning_yes": 1 if airconditioning == "yes" else 0,
    "parking": parking,
    "prefarea_yes": 1 if prefarea == "yes" else 0,
}

# Convert to DataFrame and ensure correct feature order
input_df = pd.DataFrame([[input_dict[col] for col in feature_order]], columns=feature_order)

# Predict
if st.button("Predict Price"):
    price = model.predict(input_df)[0]
    st.success(f"Predicted Price: ₹{price:,.2f}")
    st.session_state.history.append({"Input": input_dict, "Prediction": price})

# Show history
if st.checkbox("Show Prediction History"):
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)
    else:
        st.info("No predictions yet.")
