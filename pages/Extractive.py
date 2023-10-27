import streamlit as st
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string

# Import nltk and download necessary data
import nltk
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
        response = requests.get(pdf_url)
        response.raise_for_status()
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

        # Define a function to count characters in the text
        def count_characters(text):
            return len(text) if text is not None else 0

        # Calculate the target summary length based on the original text
        original_text_length = count_characters(file_content)
        st.text(f"Original text length: {original_text_length} characters")

        # Tokenize the text
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(file_content)
        tokens = [token.text for token in doc]

        # Remove stop words and punctuation
        filtered_tokens = [token for token in tokens if token.lower() not in STOP_WORDS and token not in string.punctuation]

        # Calculate the number of tokens based on the selected summarization percentage
        selected_tokens = int(len(filtered_tokens) * summarization_percentage / 100)

        # Combine the filtered tokens into a summarized text
        summarized_text = " ".join(filtered_tokens[:selected_tokens])
        st.text(f"Summarized Text ({summarization_percentage}%):")
        st.write(summarized_text)
        st.success("Summarization complete!")

    else:
        st.error("Failed to summarize the PDF from the provided URL.")

