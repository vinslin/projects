import streamlit as st
import fitz
from PIL import Image
import pytesseract
from mtranslate import translate
import os
import random


def save_uploaded_file(uploaded_file, folder_path):
    if uploaded_file is not None:
        # Create the output directory if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the uploaded file to the specified folder
        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        return file_path
    else:
        return None

def create_random_text_file(output_directory,name):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Generate a random number for the filename
    random_number = random.randint(1, 10)

    # Filename with the random number and .txt extension
    random_filename = f"{name}{random_number}.txt"

    # Path to the new text file
    output_file_path = os.path.join(output_directory, random_filename)

    # Create the new text file
    with open(output_file_path, 'w') as file:
        file.write(" ")

    return output_file_path
# Function to translate a single line from English to Tamil

def translate_to_tamil(line):
    try:
        translated_text = translate(line, 'ta', 'auto')
        if translated_text.strip() == '':
            return None
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return None   
# Function to split PDF into images and extract text from them


def split_pdf_and_extract_text(pdf_file, output_txt_path):
    # Open the output text file in append mode
    try:
        with open(output_txt_path, "a", encoding="utf-8") as output_txt_file:
            # Open the PDF document
            pdf_document = fitz.open(pdf_file)

            # Iterate over each page in the PDF
            for page_num in range(len(pdf_document)):
                # Get the page
                page = pdf_document.load_page(page_num)

                # Render the page as a Pixmap
                pixmap = page.get_pixmap()

                # Convert the Pixmap to a PIL Image object
                image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

                # Extract text from the image using Tesseract
                extracted_text = pytesseract.image_to_string(image)

                # Translate the line to Tamil
                translated_line = translate_to_tamil(extracted_text)

                # Write the extracted text to the output text file
                output_txt_file.write(f"=== Page {page_num+1} ===\n")
                output_txt_file.write(extracted_text)
                output_txt_file.write("\n\n")
                output_txt_file.write("\n\n")
                output_txt_file.write(f"=== Page {page_num+1} ===\n")
                st.write(f"=== Page {page_num+1} ===\n")
                st.write(translated_line)
                output_txt_file.write("\n\n")
                if translated_line is not None:
                    output_txt_file.write(translated_line)
                    output_txt_file.write("\n\n")

            # Close the PDF document
            pdf_document.close()
    except Exception as e:
        print(f"An error occurred: {e}")



# Define input PDF file path
#pdf_path = 'input.pdf'

# Define output text file path
output_txt_path = 'output.txt'

# Call the function to split PDF into images and extract text
#split_pdf_and_extract_text(pdf_path, output_txt_path)



st.markdown("<h1 style='text-align: center;'>PDF TRANSLATOR</h1>", unsafe_allow_html=True)
st.title('')
image = Image.open(r"img.png")
st.image(image, use_column_width=True)

 # Upload PDF file
pdf_path  = st.file_uploader("Upload a PDF file", type="pdf")

output_folder = "uploaded_pdf"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


    # If PDF file is uploaded
if pdf_path is not None:
        # Display file details
       

       # Save the uploaded file automatically
        pdf_path = save_uploaded_file(pdf_path, output_folder)
        
        st.write("Uploaded PDF file:", pdf_path)
        output_directory = "output_files"
        #file_name = "input.pdf"
        #name_without_extension = pdf_path.name.split(".")[0]
          # Output: input

        name_without_extension = os.path.basename(os.path.dirname(pdf_path))
        # Call the function to create the text file
        txtpath=create_random_text_file(output_directory,name_without_extension)
        
        # Extract text from PDF
        text = split_pdf_and_extract_text(pdf_path,txtpath)

        # Display extracted text
        st.write("DONE")
        #st.write(text)

        # Save extracted text to text file
       # with open("extracted_text.txt", "w", encoding="utf-8") as f:
       #     f.write(text)
        st.success("Text extracted and saved to 'OUTPUT_FILES FOLDER'")


