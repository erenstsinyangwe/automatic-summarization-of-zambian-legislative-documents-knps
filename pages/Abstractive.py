import subprocess
import streamlit as st
import requests
from pdfminer.high_level import extract_text
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Install required packages
subprocess.run(['pip', 'install', 'transformers[sentencepiece]', 'pdfminer.six'])
subprocess.run(['pip', 'install', 'torch'])

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
    if st.button("Summarize"):
        with st.empty():
            st.text("Summarizing... Please wait.")
            try:
                pdf_text = extract_text_from_pdf(pdf_file_path)
            except Exception as e:
                st.error(f"Summarization failed: {str(e)}")
                pdf_text = None
else:
    text_input = st.text_area("Enter the text:")
    if st.button("Summarize"):
        with st.empty():
            st.text("Summarizing... Please wait.")
            pdf_text = text_input

# Check if text is available
if pdf_text is not None:
    # Initialize Hugging Face models
    checkpoint = "nsi319/legal-pegasus"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

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

# Define pdf_text
pdf_text = None  # Initialize pdf_text as None

# Run Streamlit app
if __name__ == "__main__":
    st.run_app()
