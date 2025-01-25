from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model_path = "model.pkl"
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading the model: {e}")

@app.route('/')
def home():
    return render_template('index.html')  # This will render your HTML form

@app.route('/predict', methods=['POST'])
def predict():
    # Extracting data from the form
    try:
        features = [
            float(request.form['product_id']),
            float(request.form['category_name']),
            float(request.form['quantity']),
            float(request.form['total_price']),
            float(request.form['freight_price']),
            float(request.form['name_length']),
            float(request.form['description_length']),
            float(request.form['photo_quantity']),
            float(request.form['weight']),
            float(request.form['score']),
            float(request.form['customers']),
            int(request.form['weekday']),
            int(request.form['weekend']),
            int(request.form['holiday']),
            int(request.form['month']),
            int(request.form['year']),
            float(request.form['s']),
            float(request.form['volume']),
            float(request.form['comp1']),
            float(request.form['fp1']),
            float(request.form['comp2']),
            float(request.form['ps2']),
            float(request.form['fp2']),
            float(request.form['comp3']),
            float(request.form['ps3']),
            float(request.form['fp3']),
            float(request.form['lag_price'])
        ]
        
        # Reshape for prediction
        input_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_array)
        return jsonify({'Predicted Price': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)