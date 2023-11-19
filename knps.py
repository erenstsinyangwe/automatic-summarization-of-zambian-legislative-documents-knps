import streamlit as st
from modules.pdf_text_extractor import extract_text_from_pdf_url
from modules.text_processor import process_text
from modules.summarizer import abstractive_summarize
from requests.exceptions import ConnectionError

def main():
    st.set_page_config(page_title="Zambian Summarization App", page_icon="📜", layout="wide")

    # Section for PDF Text Extraction
    st.header("PDF Text Extraction")

    # User input: PDF URL
    pdf_url = st.text_input("Enter the PDF URL:")

    # User input: Desired percentage for the summary length
    summary_percentage = st.slider("Select the desired percentage for the summary length", 1, 100, 20, 1)

    # Extract text when the user clicks the button
    if st.button("Extract Text"):
        # Display extraction message
        extract_message = st.empty()
        extract_message.info("Extracting text from the PDF. Please wait...")

        try:
            # Extract text
            extracted_text = extract_text_from_pdf_url(pdf_url)

            # Update or delete extraction message
            if extracted_text:
                extract_message.success("Text extraction complete.")
            else:
                extract_message.error("Failed to extract text from the PDF. Please check the URL.")
                # Stop further processing if extraction fails
                return

            # Process the extracted text
            process_message = st.empty()
            process_message.info("Processing the extracted text...")

            processed_text = process_text(extracted_text)

            # Update or delete processing message
            if processed_text:
                process_message.success("Text processing complete.")
            else:
                process_message.error("Text processing failed. Please check the input text.")
                # Stop further processing if text processing fails
                return

            # Summarize the processed text with the specified percentage
            summary_message = st.empty()
            summary_message.info("Generating text summary...")

            summary = abstractive_summarize(processed_text, summary_percentage)

            # Display the processed text and summary
            if summary:
                summary_message.success("Text summarization complete.")
                st.header("Text Summary")
                st.text(summary)
            else:
                summary_message.error("Text summarization failed. Please check the processed text.")

        except ConnectionError:
            st.error("Connection Error: Please check your internet connection and try again.")

if __name__ == "__main__":
    main()