import subprocess
import streamlit as st
import requests
from pdfminer.high_level import extract_text
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Install required packages
required_packages = ['transformers[sentencepiece]', 'pdfminer.six', 'torch']
subprocess.run(['pip', 'install'] + required_packages)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    response = requests.get(pdf_file_path)
    with open("temp.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return extract_text("temp.pdf").strip()

# Initialize the pdf_text variable
pdf_text = None

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

# Check if the pdf_text variable is empty
if pdf_text is not None:
    # Initialize Hugging Face models
    checkpoint = "nsi319/legal-pegasus"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

    # Tokenize and summarize the text
    sentences = pdf_text.split(".")
    chunks = [sentence for sentence in sentences if len(tokenizer.tokenize(sentence)) + len(tokenizer.tokenize("Summary:")) <= tokenizer.model_max_length]

    # Generate and display the model's output for each input
    st.header("Summarized Text:")
    for chunk in chunks:
        output = model.generate(tokenizer.encode("Summary: " + chunk, return_tensors="pt"))
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        st.write(generated_text)

    st.text("Summarization complete.")

# Run Streamlit app
if _name_ == "_main_":
    st.run_app()
