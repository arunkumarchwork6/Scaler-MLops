from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model_filename = 'regression_model.pkl'

# Check if model file exists
if not os.path.exists(model_filename):
    print(f"Error: {model_filename} not found. Please run regression_model.py first.")
    model = None
else:
    with open(model_filename, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded successfully from '{model_filename}'")

# Feature names from the diabetes dataset (you can modify these for your data)
FEATURE_NAMES = [
    'age',
    'sex',
    'body mass index',
    'average blood pressure',
    'total serum cholesterol',
    's1',
    's2',
    's3',
    's4',
    's5'
]

@app.route('/')
def index():
    """Render the home page with prediction form"""
    return render_template('index.html', features=FEATURE_NAMES)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to make predictions"""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        # Extract features in the correct order
        features = []
        for feature in FEATURE_NAMES:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            features.append(float(data[feature]))
        
        # Convert to numpy array and reshape for prediction
        input_data = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict-form', methods=['POST'])
def predict_form():
    """Handle form submission and return HTML response"""
    try:
        if model is None:
            return "Error: Model not loaded", 500
        
        # Extract form data
        features = []
        for feature in FEATURE_NAMES:
            if feature not in request.form:
                return f"Error: Missing feature {feature}", 400
            features.append(float(request.form[feature]))
        
        # Convert to numpy array and reshape for prediction
        input_data = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return render_template('result.html', 
                             prediction=round(prediction, 2),
                             features=dict(zip(FEATURE_NAMES, features)))
    
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
