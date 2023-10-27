import streamlit as st
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
import string
from heapq import nlargest

# Download NLTK data for tokenization
nltk.download('punkt')

# Declare a global variable to store the extracted text
file_content = None

# Define the Streamlit app title
st.title("Zambian Automatic Legislative Document Summarizer")

# Create a text input field for the PDF URL
pdf_url = st.text_input("Enter PDF URL:")

# Create radio buttons for summarization percentage
summarization_percentage = st.radio("Select Summarization Percentage", [10, 20, 25, 30, 50])

# Define a function to extract text from a PDF URL
def extract_text_from_url(pdf_url):
    try:
        # Fetch the PDF content from the provided URL
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Convert the PDF content into a readable text format
        pdf_stream = BytesIO(response.content)
        pdf_text = extract_text(pdf_stream)

        return pdf_text
    except Exception as e:
        return None

# Check if the "Summarize" button is clicked
if st.button("Summarize"):
    pdf_text = extract_text_from_url(pdf_url)
    file_content = pdf_text

    if file_content:
        st.text("Summarized Text:")

        # Prepare NLP processing
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(file_content)

        # Calculate word frequencies
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in string.punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

        # Find the maximum word frequency
        max_frequency = max(word_frequencies.values())

        # Normalize word frequencies
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / max_frequency

        # Tokenize text into sentences
        sentence_tokens = [sent for sent in doc.sents]

        # Calculate sentence scores for summarization
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

        # Calculate the number of sentences to include in the summary
        select_length = int(len(sentence_tokens) * (summarization_percentage / 100))