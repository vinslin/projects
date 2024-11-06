import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import torch
from ultralytics import YOLO
import numpy as np
import cv2

# Load YOLOv8 model
model = YOLO("best.pt")  # Ensure 'best.pt' is your trained YOLO model

# Center-align the title using HTML
st.markdown(
    """
    <h1 style="text-align: center;">Kidney Stone Object Detection App</h1>
    """, 
    unsafe_allow_html=True
)

st.image("X-Ray.jpg", use_column_width=True)

st.write("Upload an image, and the model will detect objects and display bounding boxes with confidence levels.")

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Detecting objects...")

    # Perform inference on the image
    results = model(image)
    
    # Convert the image to an OpenCV-compatible format
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # Draw bounding boxes with only confidence scores
    for obj in results[0].boxes:
        # Extract bounding box coordinates and confidence
        x1, y1, x2, y2 = map(int, obj.xyxy[0].tolist())  # Bounding box coordinates
        confidence = obj.conf.item()  # Confidence level as a float

        # Draw bounding box
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box with thickness 2

        # Add confidence level text above the box
        label = f"{confidence:.2f}"
        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img_cv, (x1, y1 - label_height - baseline), (x1 + label_width, y1), (255, 0, 0), -1)  # Filled box for label background
        cv2.putText(img_cv, label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # White text for confidence

    # Convert back to RGB for Streamlit display
    img_result = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    detected_img = Image.fromarray(img_result)

    # Display the output image
    st.image(detected_img, caption='Detected Image with Confidence Levels', use_column_width=True)

else:
    st.write("Please upload an image to continue.")
