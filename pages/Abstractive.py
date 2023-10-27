import streamlit as st
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Declare a global variable to store the extracted text
FileContent = None

# Define the Streamlit app title
st.title("Zambian Automatic Legislative Document Summarizer")

# Create a text input field for the PDF URL
pdf_url = st.text_input("Enter PDF URL:")

# Define a function to extract text from a PDF URL
def extract_text_from_url(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_stream = BytesIO(response.content)
        pdf_text = extract_text(pdf_stream)
        return pdf_text
    except Exception as e:
        return None

# Check if the "Extract Text" button is clicked
if st.button("Summarize"):
    pdf_text = extract_text_from_url(pdf_url)
    FileContent = pdf_text

    if FileContent:
        st.text("Summarized Text:")

        # Define a function to count characters in the text
        def count_characters(text):
            return len(text) if text is not None else 0

        # Show the total number of characters in the extracted text
        total_characters = count_characters(FileContent)
        st.text(f"Total characters in the extracted text: {total_characters}")

        st.info("Summarizing the document...")

        checkpoint = "nsi319/legal-led-base-16384"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

        nltk.download('punkt')  # Move nltk download outside the loop

        sentences = nltk.tokenize.sent_tokenize(FileContent)

        # Create the chunks
        length = 0
        chunk = ""
        chunks = []

        for sentence in sentences:
            combined_length = len(tokenizer.tokenize(sentence)) + length
            if combined_length <= tokenizer.model_max_length:
                chunk += sentence + " "
                length = combined_length

                if sentence == sentences[-1]:
                    chunks.append(chunk.strip())
            else:
                chunks.append(chunk.strip())
                length = 0
                chunk = ""
                chunk += sentence + " "
                length = len(tokenizer.tokenize(sentence))

        # Generate summaries and display them
        st.info("Generating summaries...")

        def generate(inputs, model, tokenizer):
            output = model.generate(**inputs)
            return tokenizer.decode(output[0], skip_special_tokens=True)

        for input_text in chunks:
            input_dict = tokenizer(input_text, return_tensors="pt")
            summary = generate(input_dict, model, tokenizer)
            st.write(summary)
    else:
        st.error("Failed to summarize your PDF from the link you provided.")