import streamlit as st
import requests
from pdfminer.high_level import extract_text
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Define a function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    response = requests.get(pdf_file_path)
    with open("temp.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return extract_text("temp.pdf").strip()


# Streamlit app
st.title("Text Summarizer")

# User input for PDF link or text
input_type = st.radio("Choose input type:", ("PDF Link", "Text Input"))
if input_type == "PDF Link":
    pdf_file_path = st.text_input("Enter the link to the PDF file:")
elif input_type == "Text Input":
    text_input = st.text_area("Enter the text:")

# Check if text is available
if pdf_file_path or text_input:
    # Initialize Hugging Face models
    checkpoint = "nsi319/legal-pegasus"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

    # Get the text to summarize
    if pdf_file_path:
        pdf_text = extract_text_from_pdf(pdf_file_path)
    else:
        pdf_text = text_input

    # Tokenize and summarize the text
    sentences = pdf_text.split(".")
    chunks = []
    for sentence in sentences:
        combined_length = len(tokenizer.tokenize(sentence)) + len(tokenizer.tokenize("Summary:"))
        if combined_length <= tokenizer.model_max_length:
            chunks.append(sentence)

    # Generate and display the model's output for each input
    st.header("Summarized Text:")
    for chunk in chunks:
        output = model.generate(tokenizer.encode("Summary: " + chunk, return_tensors="pt"))
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        st.write(generated_text)
    st.text("Summarization complete.")
