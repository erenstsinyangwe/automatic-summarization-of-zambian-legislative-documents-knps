import streamlit as st
from io import BytesIO
from pdfminer.high_level import extract_text
import requests

def extract_text_from_pdf_url(pdf_url):
    try:
        with st.spinner("Extracting text..."):
            # Fetch PDF content from the URL
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            pdf_content = BytesIO(response.content)

            # Extract text from PDF
            text = extract_text(pdf_content)
            return text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("PDF Text Extractor")

    # Get PDF link from user
    pdf_url = st.text_input("Paste PDF link:")

    if st.button("Extract Text"):
        if pdf_url:
            # Extract text from PDF link
            text = extract_text_from_pdf_url(pdf_url)

            if text:
                # Display extracted text
                st.subheader("Extracted Text:")
                st.text_area("Text from PDF", text, height=400)
        else:
            st.warning("Please paste a PDF link.")

if __name__ == "__main__":
    main()
