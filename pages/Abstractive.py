import streamlit as st
import requests
import re
import string
from pdfminer.high_level import extract_text
import nltk

# Set custom CSS for better styling
st.write(
    """
    <style>
    .summary-text {
        color: #333;
        background-color: #e5e5e5;
        padding: 10px;
        border-radius: 5px;
    }
    .statistics-text {
        color: #666;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
    .meter-label {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Download NLTK data
nltk.download("punkt")

def extract_pdf_text(pdf_link: str) -> str:
    try:
        response = requests.get(pdf_link)
        with open("temp.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        text = extract_text("temp.pdf")
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF file: {e}")
    return text

def remove_stand_alone_numbers(text: str) -> str:
    # Use regex to remove standalone numbers while preserving meaningful numbers within text
    return re.sub(r'(?<=\s)\d+(?=\s)', '', text)

st.title("Abstractive Summarization")
st.write("Abstractive summarization is a technique that generates a summary of a document by interpreting and rephrasing the text. It goes beyond extracting key sentences and aims to produce human-like summaries, which may not be present in the original text.")
st.write("You can access PDFs of legislative documents from the [Zambian Parliament's website](https://www.parliament.gov.zm/acts-of-parliament).")

pdf_link = st.text_input("Enter the link to the PDF file:")
summary_percentage = st.slider("Select the percentage of content to summarize:", 0, 100, 30)

if st.button("Summarize"):
    if not pdf_link:
        st.warning("Please enter a PDF link to summarize.")
    else:
        try:
            pdf_text = extract_pdf_text(pdf_link)
            pdf_text = re.sub(r"\s+", " ", pdf_text)
            pdf_text = remove_stand_alone_numbers(pdf_text)  # Remove standalone numbers
        except Exception as e:
            st.error(f"Error: {e}")
        else:
            def summarize(text: str, per: float) -> str:
                sentences = nltk.sent_tokenize(text)
                tokens = nltk.word_tokenize(text)
                stopwords = set(string.punctuation + " ")
                word_frequencies = {}
                
                for token in tokens:
                    token = token.lower()
                    if token not in stopwords:
                        if token not in word_frequencies:
                            word_frequencies[token] = 1
                        else:
                            word_frequencies[token] += 1
                
                scores = {sentence: sum(word_frequencies.get(word, 0) for word in nltk.word_tokenize(sentence)) for sentence in sentences}
                important_sentences = sorted(sentences, key=lambda sentence: scores[sentence], reverse=True)
                
                num_sentences = max(1, int(per / 100 * len(sentences)))  # Ensure at least 1 sentence is selected
                selected_sentences = important_sentences[:num_sentences]
                
                summary = "\n\n".join(selected_sentences)  # Add line breaks for readability
                return summary

            summary = summarize(pdf_text, summary_percentage)
            
            if summary:
                # Display the summary with better readability
                st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)
                
                # Calculate statistics
                original_char_count = len(pdf_text)
                summary_char_count = len(summary)
                
                # Display statistics
                st.markdown(
                    f'<div class="statistics-text">Original Document Character Count: {original_char_count} characters</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="statistics-text">Summary Character Count: {summary_char_count} characters</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("The summary is empty.")