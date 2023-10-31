import streamlit as st
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Page configuration
st.set_page_config(
    page_title="Summarizer-KNPS",
    page_icon="📜"
)

# Declare global variables
FILE_CONTENT = None
CHECKPOINT = "nsi319/legal-pegasus"
TOKENIZER = AutoTokenizer.from_pretrained(CHECKPOINT)
MODEL = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT)

def extract_text_from_url(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_stream = BytesIO(response.content)
        pdf_text = extract_text(pdf_stream)
        return pdf_text
    except Exception as e:
        return None

def summarize_text(text, max_summary_length):
    try:
        input_dict = TOKENIZER(text, return_tensors="pt", max_length=1024, truncation=True)
        summary = MODEL.generate(
            inputs=input_dict,
            max_length=max_summary_length,
            num_beams=4,
            no_repeat_ngram_size=2,
            length_penalty=2.0,
            early_stopping=True,
        )
        return TOKENIZER.decode(summary[0], skip_special_tokens=True)
    except Exception as e:
        st.error(f"An error occurred during summarization: {e}")
        return None

def main():
    st.title("Zambian Automatic Legislative Document Summarizer")

    pdf_url = st.text_input("Enter PDF URL:")
    summarization_percentage = st.number_input(
        "Enter Summarization Percentage (e.g., 10 for 10%):",
        min_value=1,
        max_value=100,
        step=1,
        value=20
    )

    if st.button("Summarize"):
        pdf_text = extract_text_from_url(pdf_url)

        if not pdf_text:
            st.error("Summarization of the PDF from the provided URL failed. Please ensure the link to the document you want to summarize is valid and accessible.")
            return

        global FILE_CONTENT
        FILE_CONTENT = pdf_text

        max_summary_length = int(summarization_percentage / 100 * len(FILE_CONTENT))

        summary = summarize_text(FILE_CONTENT, max_summary_length)
        st.text("Summarized Text:")
        st.write(summary)

        st.success("Summarization complete!")

if __name__ == "__main__":
    main()
