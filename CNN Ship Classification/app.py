import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore", message=".*LibreSSL.*")
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU

# Load the model without recompiling
model = tf.keras.models.load_model("cnn_model_2.h5", compile=False)

# Class labels
CLASS_NAMES = ["Cargo", "Tanker", "Military", "Fishing", "Cruise"]

st.title("🚢 Ship Classification AI")
st.write("Upload an image of a ship to classify its type")

# File uploader
uploaded_file = st.file_uploader("Choose a ship image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)

    # Convert image to RGB (some formats might be grayscale)
    image = image.convert("RGB")
    
    # Resize and preprocess
    image = image.resize((128, 128))
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class = CLASS_NAMES[predicted_class_index]
    confidence = np.max(predictions) * 100

    # Apply confidence threshold
    confidence_threshold = 50
    if confidence >= confidence_threshold:
        st.success(f"**Prediction:** {predicted_class} ({confidence:.2f}% confidence)")
    else:
        st.warning("Prediction confidence is too low. Try another image.")



