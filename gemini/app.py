import streamlit as st
import pickle


import re

import requests
from bs4 import BeautifulSoup

import google.generativeai as genai



def separate_and_display_sentences(large_string):
    # Split the large string into sentences using dots as delimiters
    sentences = large_string.split(".")
    
    # Display the sentences using Streamlit's st.text function
    for sentence in sentences:
        st.text(sentence.strip())



def generate_text(prompt, model_name="gemini-pro"):
    # Replace with your actual API key
    api_key = "AIzaSyBSlif-91q43MbqYypAxPnshlKIbFGAT2c"
    genai.configure(api_key=api_key)

    # Create the model instance
    model = genai.GenerativeModel(model_name)

    # Generate the content
    response = model.generate_content(prompt)

    # Return the generated text
    return response.text

    
def get_web_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return None

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    paragraphs = soup.find_all('p')
    paragraph_texts = [paragraph.text.strip() for paragraph in paragraphs]

    temp_para=r" "
    for i in paragraph_texts:
        temp_para=temp_para+i

    modified_string =temp_para.replace('\'', '')

      

    return modified_string




st.markdown(
    """
    <h1 style='text-align: center;'>ARTICLE ANALYSIS</h1>
    """,
    unsafe_allow_html=True
)

file_path = "Marketing_Tracking-Links_Site_0409.png"
st.image(file_path)

url= st.text_area("Enter the link here")

if st.button('SUMMARIZE'):
    web_page_content = get_web_page_content(url)
    paragraphs = extract_data(web_page_content)
    temp="summarize this article in 200 words"
    new=paragraphs+temp
    
    st.text("HERE WE GOOOOOOOOO!!!!")
    summary=generate_text(new)
    
    st.header("SUMMARIZED VERSION")
    st.markdown(summary)




new= st.text_area("Enter the question here")
if st.button('question about article'):
    ans=generate_text(new)
    st.markdown(ans)

    
 


    

        
    
    
