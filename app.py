import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Set Page Configuration
st.set_page_config(
    page_title="AI Driven Yield Prediction",
    page_icon="🌱",
    layout="wide"
)

# Title and Tagline
st.markdown("<h1 style='text-align: center;'>AI Driven Yield Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Revolutionizing agriculture with data-driven insights</h3>", unsafe_allow_html=True)

soil_type = ["Peaty", "Clay", "Silty Clay", "Loam", "Sandy Loam", "Chalky", "Sandy", "Loamy Sand", "Silt Loam", "Clay Loam"]
crop = ["Wheat", "Rice", "Soybean", "Cotton", "Maize"]

# Function to encode categorical inputs safely
def encode_feature(encoder_dict, feature_name, value, options_list):
    if feature_name in encoder_dict:
        return encoder_dict[feature_name].transform([value])[0]
    else:
        return options_list.index(value)

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        Soil_Type = st.selectbox("Soil_Type", options=soil_type, help="Select the Soil Type")
        Crop = st.selectbox("Crop", options=crop, help="Select the Crop")
        Rainfall_mm = st.number_input("Rainfall_mm", min_value=50, max_value=4000, step=1)

    with col2:
        Temperature_Celsius = st.number_input("Temperature_Celsius", min_value=-20.0, max_value=50.0, step=0.5)
        Fertiliser_Quantity = st.number_input("Fertiliser_Quantity", min_value=0.0, max_value=150000.0, step=0.5)
        Pesticide_Quantity = st.number_input("Pesticide_Quantity", min_value=0.0, max_value=1000.0, step=0.01)

    Land_Area = st.number_input("Land_Area", min_value=0.1, max_value=100.0, step=0.1)

    submit_button = st.form_submit_button("Predict Yield")

# Processing Prediction
if submit_button:
    try:
        with open("modelcheck.pkl", "rb") as file:
            model_data = pickle.load(file)
        model = model_data["model"]
        label_encoders = model_data["encoder"]
        scaler = model_data["scaler"]  # Load the scaler

        soil_type_encoded = encode_feature(label_encoders, "Soil_Type", Soil_Type, soil_type)
        crop_encoded = encode_feature(label_encoders, "Crop", Crop, crop)

        # Defining Column Names based on the features used in training
        feature_columns = ["Soil_Type", "Crop", "Rainfall_mm", "Temperature_Celsius", "Fertiliser_Quantity", "Pesticide_Quantity"]

        # Preparing Input Features as a DataFrame to match the training format
        input_features_df = pd.DataFrame([[soil_type_encoded, crop_encoded, Rainfall_mm, Temperature_Celsius, Fertiliser_Quantity, Pesticide_Quantity]],
                                         columns=feature_columns)

        # Standardizing Input Features
        input_features_scaled = scaler.transform(input_features_df)

        # Make Prediction
        predicted_yield = model.predict(input_features_scaled)[0]
        st.success(f"Predicted Crop Yield: {predicted_yield:.2f} tonnes per acre")
        st.success(f"Total Crop Yield : {predicted_yield * Land_Area:.2f} tonnes")

    except Exception as e:
        st.error(f"An Error Occurred: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2025 AI Driven Yield Prediction | Powered by Advanced Agricultural Analytics</p>", unsafe_allow_html=True)
