import streamlit as st
import pandas as pd
from joblib import load

# Load trained model
model = load("random_forest_model.joblib")

# Exact feature list from training
feature_order = [
    'area', 'bedrooms', 'bathrooms', 'stories', 'parking',
    'mainroad_no', 'mainroad_yes',
    'guestroom_no', 'guestroom_yes',
    'basement_no', 'basement_yes',
    'hotwaterheating_no', 'hotwaterheating_yes',
    'airconditioning_no', 'airconditioning_yes',
    'prefarea_no', 'prefarea_yes',
    'furnishingstatus_furnished',
    'furnishingstatus_semi-furnished',
    'furnishingstatus_unfurnished'
]

# Initialize history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Housing Price Prediction")
st.write("Enter house details to get a price estimate.")

# Inputs
area = st.number_input("Area (sq ft)", 200, 10000, value=1200)
bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Bathrooms", [1, 2, 3])
stories = st.selectbox("Stories", [1, 2, 3])
parking = st.slider("Parking Spaces", 0, 5, 1)

mainroad = st.radio("Main Road Access", ["yes", "no"])
guestroom = st.radio("Guest Room", ["yes", "no"])
basement = st.radio("Basement", ["yes", "no"])
hotwaterheating = st.radio("Hot Water Heating", ["yes", "no"])
airconditioning = st.radio("Air Conditioning", ["yes", "no"])
prefarea = st.radio("Preferred Area", ["yes", "no"])
furnishing = st.radio("Furnishing Status", ["furnished", "semi-furnished", "unfurnished"])

# Create full input dict with all dummy columns
input_dict = {
    'area': area,
    'bedrooms': bedrooms,
    'bathrooms': bathrooms,
    'stories': stories,
    'parking': parking,

    'mainroad_yes': 1 if mainroad == 'yes' else 0,
    'mainroad_no': 1 if mainroad == 'no' else 0,

    'guestroom_yes': 1 if guestroom == 'yes' else 0,
    'guestroom_no': 1 if guestroom == 'no' else 0,

    'basement_yes': 1 if basement == 'yes' else 0,
    'basement_no': 1 if basement == 'no' else 0,

    'hotwaterheating_yes': 1 if hotwaterheating == 'yes' else 0,
    'hotwaterheating_no': 1 if hotwaterheating == 'no' else 0,

    'airconditioning_yes': 1 if airconditioning == 'yes' else 0,
    'airconditioning_no': 1 if airconditioning == 'no' else 0,

    'prefarea_yes': 1 if prefarea == 'yes' else 0,
    'prefarea_no': 1 if prefarea == 'no' else 0,

    'furnishingstatus_furnished': 1 if furnishing == 'furnished' else 0,
    'furnishingstatus_semi-furnished': 1 if furnishing == 'semi-furnished' else 0,
    'furnishingstatus_unfurnished': 1 if furnishing == 'unfurnished' else 0
}

# Create input DataFrame
input_df = pd.DataFrame([[input_dict[col] for col in feature_order]], columns=feature_order)

# Predict
if st.button("Predict Price"):
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted House Price: ₹{prediction:,.2f}")
    st.session_state.history.append({"Input": input_dict, "Predicted Price": prediction})

# Show prediction history
if st.checkbox("Show Prediction History"):
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history))
    else:
        st.info("No predictions yet.")
