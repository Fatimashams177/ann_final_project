import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# Load trained model (Random Forest)
model = load("random_forest_model.joblib")

# Initialize session state for storing prediction history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Housing Price Prediction App")
st.write("Enter the housing features to predict the price.")

# Input fields for prediction (adjust based on your actual dataset)
area = st.number_input("Area (sq ft)", min_value=200, max_value=10000, value=1200)
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

# Create input dictionary with one-hot encoding
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

# Convert to DataFrame
input_df = pd.DataFrame([input_dict])

# Make sure column order matches model training
expected_features = model.feature_names_in_
for col in expected_features:
    if col not in input_df.columns:
        input_df[col] = 0  # fill missing dummy variables with 0

input_df = input_df[expected_features]

# Predict and store result
if st.button("Predict Price"):
    predicted_price = model.predict(input_df)[0]
    st.success(f"Predicted Price: ₹{predicted_price:,.2f}")

    # Save prediction history
    st.session_state.history.append({
        "Input": input_dict,
        "Prediction": predicted_price
    })

# Show history
if st.checkbox("Show Prediction History"):
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)
    else:
        st.info("No predictions yet.")
