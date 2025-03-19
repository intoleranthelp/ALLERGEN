from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load the trained model
MODEL_PATH = "gel_classifier.h5"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file '{MODEL_PATH}' not found. Train and save the model first!")

model = tf.keras.models.load_model(MODEL_PATH)
classes = ["No Allergy", "Peanut Allergy", "Lactose Intolerance"]

# Ensure the uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        print("❌ No file received")
        return jsonify({'error': 'No file received'}), 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    print(f"✅ File saved at: {filepath}")

    # Load and process the image
    img = cv2.imread(filepath)
    if img is None:
        print("❌ Error loading image")
        return jsonify({'error': 'Invalid image file'}), 400

    img = cv2.resize(img, (150, 150))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Make a prediction
    prediction = model.predict(img)
    probabilities = prediction[0].tolist()

    # Debugging output
    print(f"🔹 Model Prediction Raw: {prediction}")
    print(f"🔹 Converted Probabilities: {probabilities}")

    if not probabilities:
        print("❌ No prediction received")
        return jsonify({'error': 'No prediction received'}), 500

    response = {
        'No Allergy': f"{probabilities[0] * 100:.2f}%",
        'Peanut Allergy': f"{probabilities[1] * 100:.2f}%",
        'Lactose Intolerance': f"{probabilities[2] * 100:.2f}%",
        'final_prediction': classes[np.argmax(probabilities)]
    }

    print(f"✅ Final Prediction Sent: {response}")
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
