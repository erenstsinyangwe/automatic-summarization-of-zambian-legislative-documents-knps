
python
import streamlit as st
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
import string

# Download NLTK data for tokenization
nltk.download('punkt')

# Define a function to extract text from a PDF URL
def extract_text_from_url(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()

    pdf_stream = BytesIO(response.content)
    pdf_text = extract_text(pdf_stream)

    return pdf_text

# Define a function to calculate word frequencies
def calculate_word_frequencies(doc):
    stopwords = list(STOP_WORDS)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in string.punctuation:
            if word.text not in word_frequencies:
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    return word_frequencies

# Define a function to calculate sentence scores for summarization
def calculate_sentence_scores(sentence_tokens, word_frequencies):
    sentence_scores = {}
    for sent in sentence_tokens:
        score = sum(word_frequencies.get(word.text.lower(), 0) for word in sent)
        sentence_scores[sent] = score

    return sentence_scores

# Define a function to generate a summary
def generate_summary(sentence_tokens, sentence_scores, select_length):
    sorted_sentences = sorted(sentence_tokens, key=lambda x: sentence_scores[x], reverse=True)
    summary = sorted_sentences[:select_length]

    return summary

# Define the Streamlit app
if __name__ == '__main__':
    # Set the page configuration
    st.set_page_config(
        page_title="Zambian Automatic Legislative Document Summarizer",
        page_icon="📜"
    )

    # Create a text input field for the PDF URL
    pdf_url = st.text_input("Enter PDF URL:")

    # Create radio buttons for summarization percentage
    summarization_percentage = st.radio("Select Summarization Percentage", [10, 20, 25, 30, 50])

    # Check if the "Summarize" button is clicked
    if st.button("Summarize"):
        pdf_text = extract_text_from_url(pdf_url)

        if pdf_text:
            # Prepare NLP processing
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(pdf_text)

            # Calculate word frequencies
            word_frequencies = calculate_word_frequencies(doc)

            # Tokenize text into sentences
            sentence_tokens = list(doc.sents)

            # Calculate sentence scores
            sentence_scores = calculate_sentence_scores(sentence_tokens, word_frequencies)

            # Generate a summary
            summary = generate_summary(sentence_tokens, sentence_scores, int(len(sentence_tokens) * (summarization_percentage / 100)))

            # Display the summary
            st.text("Summarized Text:")
            st.markdown('\n'.join(map(str, summary)))
