import streamlit as st
import pandas as pd
from joblib import load

# Load the trained model
model = load("random_forest_model.joblib")

# Feature list (exactly as used during training)
feature_order = [
    'area', 'bedrooms', 'bathrooms', 'stories',
    'mainroad_yes', 'guestroom_yes', 'basement_yes',
    'hotwaterheating_yes', 'airconditioning_yes',
    'parking', 'prefarea_yes'
]

# Initialize prediction history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Housing Price Predictor")
st.write("Enter the house details to estimate its market price.")

# Input fields
area = st.number_input("Area (sq ft)", 200, 10000, value=1200)
bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Bathrooms", [1, 2, 3])
stories = st.selectbox("Stories", [1, 2, 3])
mainroad = st.selectbox("Main Road Access", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
parking = st.slider("Parking Spaces", 0, 5, value=1)
prefarea = st.selectbox("Preferred Area", ["yes", "no"])

# Create input dictionary with binary encoding for categorical variables
input_dict = {
    'area': area,
    'bedrooms': bedrooms,
    'bathrooms': bathrooms,
    'stories': stories,
    'mainroad_yes': 1 if mainroad == 'yes' else 0,
    'guestroom_yes': 1 if guestroom == 'yes' else 0,
    'basement_yes': 1 if basement == 'yes' else 0,
    'hotwaterheating_yes': 1 if hotwaterheating == 'yes' else 0,
    'airconditioning_yes': 1 if airconditioning == 'yes' else 0,
    'parking': parking,
    'prefarea_yes': 1 if prefarea == 'yes' else 0,
}

# Ensure the input DataFrame matches the training format
input_df = pd.DataFrame([[input_dict[feat] for feat in feature_order]], columns=feature_order)

# Make prediction
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted House Price: ₹{prediction:,.2f}")

        # Save to history
        st.session_state.history.append({"Input": input_dict, "Predicted Price": prediction})

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# Show prediction history
if st.checkbox("Show Prediction History"):
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)
    else:
        st.info("No predictions yet.")
