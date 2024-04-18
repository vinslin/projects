import streamlit as st
import numpy as np
import pickle
from lightgbm import LGBMClassifier
from PIL import Image


# Load the saved model from file
with open('lgbm_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Now you can use 'loaded_model' to make predictions or perform other tasks


def main():
    st.markdown("<h1 style='text-align: center;'>Crop Recommendation App</h1>", unsafe_allow_html=True)
    image = Image.open("img.jpg")  # Replace "path_to_your_image.jpg" with the path to your image file

# Display the image
    st.image(image, caption=' ', use_column_width=True)

   

# Get user input for the seven values
    feature1 = st.number_input('Enter Nitrogen level', min_value=0.0, max_value=140.0, value=33.0)
    feature2 = st.number_input('Enter Phosphorous level', min_value=5.0, max_value=150.0, value=14.0)
    feature3 = st.number_input('Enter Potassium level', min_value=5.0, max_value=210.0, value=35.0)
    feature4 = st.number_input('Enter Temperature', min_value=5.0, max_value=50.0, value=27.148653)
    feature5 = st.number_input('Enter Humidity', min_value=10.0, max_value=100.0, value=96.663552)
    feature6 = st.number_input('Enter pH Level', min_value=2.0, max_value=15.0, value=6.027707)
    feature7 = st.number_input('Enter Rainfall', min_value=10.0, max_value=350.0, value=149.24335)


    #Create a numpy array with the user input
    test = np.array([feature1, feature2, feature3, feature4, feature5, feature6, feature7])

    # Reshape the data to a 2D array with a single sample
    test_reshaped = test.reshape(1, -1)
   
    # Predict button
    if st.button('Predict'):
        # Make predictions using the reshaped data
        prediction = loaded_model.predict(test_reshaped)

        # Display the prediction
        st.subheader('The best CROP is')
        img_path=f"{prediction[0]}.jpg"
        
        image1 = Image.open(img_path)  # Replace "path_to_your_image.jpg" with the path to your image file
        

# Display the image
        st.image(image1, caption=' ', use_column_width=True)
        
        st.markdown("<div style='display:flex; justify-content:center;'>"
                    f"<button>{prediction[0]}</button>"
                    "</div>",
                    unsafe_allow_html=True)


if __name__ == '__main__':
    main()
