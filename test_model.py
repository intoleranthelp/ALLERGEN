import tensorflow as tf
import numpy as np
import cv2
import os

# Load the trained model
MODEL_PATH = "gel_classifier.h5"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file '{MODEL_PATH}' not found! Train and save the model first.")

model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# Define class labels
classes = ["No Allergy", "Peanut Allergy", "Lactose Intolerance"]

# Choose an image to test
img_path = "C:\\Users\\kaila\\OneDrive\\Desktop\\Trial0000\\uploads\\1109.jpg"

if not os.path.exists(img_path):
    raise FileNotFoundError(f"❌ Test image '{img_path}' not found! Upload an image first.")

# Load and preprocess the image
img = cv2.imread(img_path)

if img is None:
    raise ValueError("❌ Error loading image. Check file path and format.")

# Resize image to match model input size
img = cv2.resize(img, (150, 150))

# Normalize pixel values (convert 0-255 to 0-1 range)
img = img / 255.0  

# Expand dimensions (model expects batch input)
img = np.expand_dims(img, axis=0)

# Print processed image details for debugging
print("\n🔹 Processed Image Details:")
print("   - Shape:", img.shape)
print("   - Sample Pixel Data:", img[0, 0, 0])  # Print first pixel values

# Run the image through the model
prediction = model.predict(img)
probabilities = prediction[0]  # Extract probability values

# Print probability for each class
print("\n🔹 Allergy Probabilities:")
for i, prob in enumerate(probabilities):
    print(f"   {classes[i]}: {prob * 100:.2f}%")

# Get the final prediction
final_prediction = classes[np.argmax(probabilities)]
print(f"\n✅ Final Prediction: {final_prediction}")

# Optional: Save processed image for debugging
cv2.imwrite("processed_sample.jpg", img[0] * 255)  # Convert back to 0-255 scale
print("📌 Processed image saved as 'processed_sample.jpg' for verification.")
