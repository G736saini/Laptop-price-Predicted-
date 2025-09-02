import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model and preprocessing data
try:
    with open('pipe (1).pkl', 'rb') as f:
        pipe = pickle.load(f)

    with open('pr.pkl', 'rb') as f:
        pr = pickle.load(f)

    # Debug: Print model's expected features
    st.write("Model expects these features:", pipe.feature_names_in_)
    st.write("Available columns in pr.pkl:", pr.columns.tolist())

except Exception as e:
    st.error(f"Error loading files: {str(e)}")
    st.stop()

# UI Inputs
st.title('Laptop Predictor')

# Brand selection
company_col = next((col for col in pr.columns if 'company' in col.lower()), None)
company = st.selectbox('Brand', pr[company_col].unique()) if company_col else st.error("Brand data missing")

# Type selection
type_col = next((col for col in pr.columns if 'type' in col.lower()), None)
type_name = st.selectbox('Type', pr[type_col].unique()) if type_col else st.error("Type data missing")

# RAM selection
ram_options = [4, 8, 12, 16, 32]
ram = st.selectbox('RAM (GB)', ram_options)

# Memory selection (this should match the model's expected feature name)
memory_col = 'Memory' if 'Memory' in pr.columns else next((col for col in pr.columns if 'memory' in col.lower()), None)
memory = st.selectbox('Storage (Memory)', pr[memory_col].unique()) if memory_col else st.error("Memory data missing")

# Other inputs
weight = st.number_input('Weight (kg)', min_value=0.5, max_value=5.0, value=2.0)
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
ips = st.selectbox('IPS Display', ['No', 'Yes'])
screen_size = st.number_input('Screen Size (inches)', min_value=10.0, max_value=18.0, value=15.6)
resolution = st.selectbox('Resolution', ['1920x1080', '1366x768', '1600x900', '3200x1800', '2880x1800', '2560x1600'])
cpu = st.selectbox('CPU Brand', pr['Cpu brand'].unique())
gpu = st.selectbox('GPU Brand', pr['Gpu brand'].unique())
os = st.selectbox('OS', pr['os'].unique())

if st.button('Predict Price'):
    try:
        # Process inputs
        touchscreen = 1 if touchscreen == 'Yes' else 0
        ips = 1 if ips == 'Yes' else 0
        X_res, Y_res = map(int, resolution.split('x'))
        ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

        # Create query DataFrame using model's expected feature names
        query_data = {
            'CompanyName': [company],
            'TypeOfLaptop': [type_name],
            'Ram': [ram],
            'Memory': [memory],  # Corrected from 'Mermory' to 'Memory'
            'Weight': [weight],
            'Touchscreen': [touchscreen],
            'Ips': [ips],
            'ppi': [ppi],
            'Cpu brand': [cpu],
            'Gpu brand': [gpu],
            'os': [os]
        }

        # Ensure all expected features are present
        missing_features = [f for f in pipe.feature_names_in_ if f not in query_data]
        if missing_features:
            st.error(f"Missing features: {missing_features}")
            st.stop()

        # Create DataFrame with correct column order
        query = pd.DataFrame(query_data)[pipe.feature_names_in_]

        # Make prediction
        predicted_price = pipe.predict(query)[0]
        st.success(f"Predicted Laptop Price: ₹{predicted_price:,.2f}")
        st.balloons()

    except Exception as e:
<<<<<<< HEAD
        st.error(f"Prediction failed: {str(e)}")
=======
        st.error(f"Prediction failed: {str(e)}")
>>>>>>> 2a53729ec51a8dd7c653a38e14a4b4c709d08d70
