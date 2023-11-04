import streamlit as st
import requests
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from pdfminer.high_level import extract_text

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
        except Exception as e:
            st.error(f"Error: {e}")
        else:
            def summarize(text: str, per: float) -> str:
                sentences = sent_tokenize(text)
                tokens = word_tokenize(text)
                stopwords = set(string.punctuation + " ")
                word_frequencies = {}
                
                for token in tokens:
                    token = token.lower()
                    if token not in stopwords:
                        if token not in word_frequencies:
                            word_frequencies[token] = 1
                        else:
                            word_frequencies[token] += 1
                
                scores = {sentence: sum(word_frequencies.get(word, 0) for word in word_tokenize(sentence)) for sentence in sentences}
                important_sentences = sorted(sentences, key=lambda sentence: scores[sentence], reverse=True)
                
                num_sentences = int(per / 100 * len(sentences))
                selected_sentences = important_sentences[:num_sentences]
                
                summary = " ".join(selected_sentences)
                return summary

            summary = summarize(pdf_text, summary_percentage)
            if summary:
                st.text("Summary:")
                st.write(summary)
            else:
                st.warning("The summary is empty.")