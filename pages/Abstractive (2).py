import streamlit as st
import requests
import re
from string import punctuation
from heapq import nlargest
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
    """Formats the given text by replacing multiple whitespaces with a single space and replacing newline characters with a line break."""
    # Replace multiple whitespaces with a single space
    content = re.sub(r'\s+', ' ', content)
    # Replace newline characters with a line break
    content = re.sub(r'\n', '\n', content)
    return content

# Summarize the text
def summarize(text, per):
    sentences = text.split('. ')
    word_frequencies = {}
    for sentence in sentences:
        for word in sentence.split():
            if word.lower() not in punctuation:
                if word.lower() not in word_frequencies:
                    word_frequencies[word.lower()] = 1
                else:
                    word_frequencies[word.lower()] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in sentence.split():
            if word.lower() in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word.lower()]
                else:
                    sentence_scores[sentence] += word_frequencies[word.lower()]
    select_length = int(len(sentences) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = '. '.join(summary)
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

            # Summarize the text
            summary = summarize(raw, summary_length / 100)

            # Display the summary
            st.success(summary)

if _name_ == '_main_':
    main()
