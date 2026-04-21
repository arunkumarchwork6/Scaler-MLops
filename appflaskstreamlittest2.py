import streamlit as st
import requests

st.title("Streamlit + Flask Integration")
st.write("This dashboard pulls data from a Flask API backend.")

if st.button('Refresh Data from Backend'):
    try:
        # We call the Flask URL directly
        response = requests.get("http://127.0.0.1:5000/api/data")
        
        if response.status_code == 200:
            data = response.json()
            
            # Displaying data using Streamlit components
            col1, col2, col3 = st.columns(3)
            col1.metric("Model Accuracy", f"{data['accuracy'] * 100}%")
            col2.metric("System Status", data['status'])
            col3.metric("Items Processed", data['processed_items'])
            
            st.success("Successfully fetched data from Flask!")
        else:
            st.error("Could not fetch data. Is the Flask server running?")
            
    except Exception as e:
        st.error(f"Connection Error: {e}")

st.sidebar.info("Run the Flask app first, then click the button above.")
