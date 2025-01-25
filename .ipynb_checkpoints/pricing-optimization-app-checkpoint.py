from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the trained model (ensure model.pkl exists in your project directory)
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return "Welcome to the Pricing Optimization API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input
        data = request.get_json()
        # Convert input to DataFrame
        input_df = pd.DataFrame(data)
        # Make predictions
        predictions = model.predict(input_df)
        # Return predictions as JSON
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
