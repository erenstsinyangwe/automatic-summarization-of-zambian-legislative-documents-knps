import streamlit as st
import subprocess

# Function to install requirements
def install_requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.readlines()

    for requirement in requirements:
        subprocess.run(["pip", "install", requirement], capture_output=True)

# Function to run the app
def main():
    """Summarize Zambian legislative documents."""

    # Install necessary requirements
    install_requirements()

    # Set page configuration
    st.set_page_config(
        page_title="Zambian Legislative Document Summarizer",
        page_icon="📜",
    )

    # Set background color
    st.markdown("""<style>body {background-color: #ADD8E6;}</style>""", unsafe_allow_html=True)

    # Welcome message
    st.markdown("""
        ## Zambian Legislative Document Summarizer: Summarizer-knps

        Summarize long and complex Zambian legislative documents quickly and easily.

        *Benefits:*

        - Save time.
        - Understand key points better.
        - Identify key trends and patterns.
        - Make informed decisions.

        *Try it today!*
    """)

    # Instructions
    st.markdown("""
        *How to use:*

        1. Go to the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
        2. Copy the link to the PDF document.
        3. Select the type of summary you want.
        4. Paste the link into the Summarizer-KNPS interface and select the type of summary you want.
        5. Click the "Summarize" button.
        6. Read the summary!
    """)
#....................................................................................

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import requests
from pdfminer.high_level import extract_text
import nltk

# Streamlit app
st.title("Abstractive Summarizer-knps")

# User input for PDF link
pdf_link = st.text_input("Paste the link to a PDF file:")

if st.button("Summarize"):
    # Function to extract text from PDF link
    def extract_text_from_pdf_url(pdf_url):
        try:
            pdf_response = requests.get(pdf_url)
            pdf_text = extract_text(pdf_response.content)
            return pdf_text
        except Exception as e:
            return str(e)

    # Check if PDF link is empty
    if pdf_link:
        # Extract text from the PDF link
        pdf_text = extract_text_from_pdf_url(pdf_link)

        # Store file content in a variable
        file_content = pdf_text.strip()

        # Initialize tokenizer and model
        checkpoint = "google/pegasus-large"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

        # Tokenize and summarize the content
        sentences = nltk.tokenize.sent_tokenize(file_content)
        chunks = []

        for sentence in sentences:
            chunks.append(sentence)

        # Generate summaries
        summaries = []

        for chunk in chunks:
            input_data = tokenizer(chunk, return_tensors="pt", max_length=512, truncation=True)
            output = model.generate(**input_data)
            summary = tokenizer.decode(output[0], skip_special_tokens=True)
            summaries.append(summary)

        # Display summaries in Streamlit
        for summary in summaries:
            st.write(summary)
    else:
        st.warning("Please enter a valid PDF link.")


if __name__ == "__main__":
    main()
