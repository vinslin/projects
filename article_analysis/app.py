import streamlit as st
import pickle

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict
import re

import requests
from bs4 import BeautifulSoup


    
def count_personal_pronouns(text):
    # Define a regex pattern for personal pronouns
    pronoun_pattern = re.compile(r'\b(I|we|my|ours|us)\b', flags=re.IGNORECASE)

    # Find all matches in the text
    matches = pronoun_pattern.findall(text)

    # Count the occurrences of each personal pronoun
    pronoun_counts = {pronoun.lower(): matches.count(pronoun.lower()) for pronoun in set(matches)}

    return pronoun_counts

def count_syllables(word, pronunciations):
    return max([len(list(y for y in x if y[-1].isdigit())) for x in pronunciations[word.lower()]]) if word.lower() in pronunciations else 0


def average_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    total_sentences = len(sentences)
    total_words = len(words)
    
    if total_sentences == 0:
        return 0  # Avoid division by zero
    
    average_words_per_sentence = total_words / total_sentences
    return average_words_per_sentence
    


def calculate_average_sentence_length(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

def calculate_percentage_of_complex_words(text):
    words = word_tokenize(text)
    
    return len(complex_words) / len(words)

def calculate_fog_index(average_sentence_length, percentage_of_complex_words):
    return 0.4 * (average_sentence_length + percentage_of_complex_words)



def polarity_score(modified_string):
    # Load the list from the file
    with open('lowercase_set.pkl', 'rb') as file:
        lowercase_set=pickle.load(file)

    with open('negative.pkl', 'rb') as file:
        negative = pickle.load(file)

    with open('positive.pkl', 'rb') as file:
        positive = pickle.load(file)

    words = word_tokenize(modified_string)

    # Remove stopwords
    #filtered_words = [word for word in words if word.lower() not in set(stopwords.words('english') + list(lowercase_set))]
    filtered_words = [word for word in words if word.lower() not in set(list(lowercase_set))]
    # Join the filtered words into a sentence
    filtered_text = ' '.join(filtered_words)

    # Use regular expression to remove symbols and numbers
    cleaned_string = re.sub(r'[^a-zA-Z\s]', '',filtered_text)
    v_cleaned=cleaned_string.lower()
   
    vv_cleaned= v_cleaned.split()

    positive_score=0
    for i in positive:
        for j in vv_cleaned:
           if i==j:
              positive_score+=1
 
    negative_score=0
    for i in negative:
        for j in vv_cleaned:
            if i==j:
               negative_score+=1
            
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    subjectivity_score = (positive_score + negative_score) / (len(vv_cleaned) + 0.000001)
    
    return polarity_score,subjectivity_score  
    
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







st.title('ARTICLE ANALYSIS')

url= st.text_area("Enter the link here")

if st.button('Predict'):
    web_page_content = get_web_page_content(url)
    paragraphs = extract_data(web_page_content)
    st.text("HERE WE GOOOOOOOOO!!!!")


    st.header("POLARITY SCORE")
    st.text("Polarity score measures sentiment positive or negative intensity in ARTICLE")

    st.image("polarity.png")
    st.text("  0.2 < score < 0.5  : positive")
    st.text("  0.5< score < 1     : very positive")
    st.text(" -0.2 > score > -0.5: negative")
    st.text(" -0.5 > score > -1  : very negative")
    st.text("  0.2 > score > -0.2 : neutral")
    p_score,sub_score=polarity_score(paragraphs)
    rounded_number = round(p_score, 3)
    st.subheader(rounded_number)
    if (0.2>rounded_number>-0.2):
        st.warning("NEAUTRAL")
    elif (0.2 < rounded_number < 0.5 ):
        st.success("POSITIVE")
    elif (0.5 < rounded_number < 1):
        st.success("VERY POSITIVE")
    elif (-0.2 > rounded_number > -0.5):
        st.error("NEGATIVE")
    elif (-0.2 > rounded_number > -0.5):
        st.error("VERY NEGATIVE")

    st.header(" ")
    st.header(" ")
    st.header("________OBJECTIVE OR SUBJECTIVE_______")
    st.header(" ")
    st.header(" ")
    st.image("objective-vs-subjective-meaning_3b74c0a0aa.jpg")
    st.header(" ")
    st.header(" ")
    st.subheader(round(sub_score,3))
    if (sub_score<0.25):
        st.warning("OBJECTIVE")
    elif (sub_score>=0.25 ):
        st.success("SUBJECTIVE")

    st.header(" ")
    st.header(" ")
    st.header(" ")
    st.header("________COMPLEX WORDS_______")
    # Tokenize the input string into words
    words_in_string = word_tokenize(paragraphs)

    # Load the CMU Pronouncing Dictionary
    pronunciations = cmudict.dict()

    # Filter words with more than two syllables
    more_than_four_syllables = [word for word in words_in_string if count_syllables(word, pronunciations) > 4]
    complex_words = list(set(more_than_four_syllables))
    for i in complex_words:
        st.info(i)
        
       
 


    st.header(" ")
    st.header(" ")
    st.header("________ANALYSIS OF REDABILITY_______")
    st.header(" ")
    st.image('Gunnings-fog-index-level-31.png')

    #calculate avg word per sentence
    average_words_per_sentence_value = average_words_per_sentence(paragraphs)
    

    # Calculate Average Sentence Length
    avg_sentence_length = calculate_average_sentence_length(paragraphs)
    

    # Calculate Percentage of Complex Words
    percentage_complex_words = calculate_percentage_of_complex_words(paragraphs)
   

    # Calculate Fog Index
    fog_index = calculate_fog_index(avg_sentence_length, percentage_complex_words)
    st.header(" ")
    st.error(round(fog_index))

    st.header(" ")
    st.header(" ")
    st.header("PERSONAL PRONOUNS ")
    st.header(" ")
    
    st.subheader("The lesser usage of personal pronouns denotes the Quality of an Article")
    pronoun_counts = count_personal_pronouns(paragraphs)
    st.header(" ")
    st.subheader(pronoun_counts)
        
    
    
