import streamlit as st
import requests
import re
import nltk
from nltk.tokenize import sent_tokenize
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import spacy
from pdfminer.high_level import extract_text

# Define a function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    try:
        # Get the PDF file from the specified path
        response = requests.get(pdf_file_path)
        # Write the PDF content to a temporary file
        with open("temp.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        # Extract text from the temporary file
        text = extract_text("temp.pdf")
        return text
    except Exception as e:
        return str(e)

# Format the text
def format_text(content):
    """Formats the given text by replacing `\n` with moving to the next line
    and removing any extra whitespace."""
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    # Replace `\n` with moving to the next line
    content = re.sub(r'\n', '\n', content)
    return content

# Summarize the text
def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    return summary

# Streamlit app
def main():
    # Set page title
    st.title("PDF Summarization")

    # Input link to the PDF file
    pdf_link = st.text_input("Enter the link to the PDF file")

    # Input option for the length of the summary
    summary_length = st.slider("Select the length of the summary (in percentage)", 0, 100, 50)

    # Radio button to initiate summarization
    if st.button("Summarize"):
        # Check if PDF link is provided
        if pdf_link:
            # Display progress message
            st.info("Summarization in progress...")

            # Extract text from the PDF file
            pdf_text = extract_text_from_pdf(pdf_link)

            # Store the extracted text as a string variable
            content = pdf_text.strip()

            # Format the text
            raw = format_text(content)

            # Tokenize the text into sentences
            sentences = sent_tokenize(raw)

            # Store the extracted sentences as a string variable
            text = '\n'.join(sentences)

            # Replace '\n' with moving to the next line
            text = text.replace('\n', '\n')

            # Perform summarization
            final_summary = summarize(text, summary_length/100)

            # Display success message and the summary
            st.success("Summarization successful!")
            st.text_area("Summary", value=final_summary, height=200)
        else:
            # Display error message if PDF link is not provided
            st.error("Please enter the link to the PDF file.")

# Run the Streamlit app
main()
