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
            with open("temp_pdf.pdf", "wb") as pdf_file:
                pdf_file.write(pdf_response.content)
            text = extract_text("temp_pdf.pdf")
            return text
        except Exception as e:
            return str(e)

    if pdf_link:
        # Extract text from the PDF link
        pdf_text = extract_text_from_pdf_url(pdf_link)

        # Store file content in FileContent
        FileContent = pdf_text.strip()

        # Initialize tokenizer and model
        checkpoint = "google/pegasus-large"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

        # Tokenize and summarize the content
        sentences = nltk.tokenize.sent_tokenize(FileContent)
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

# Cleanup temporary file
if "temp_pdf.pdf" in os.listdir():
    os.remove("temp_pdf.pdf")
