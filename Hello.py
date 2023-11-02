Streamlit as st
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Abstractive Summarizer-knps",
        page_icon="📜",
    )

    # Set background color
    st.markdown("""<style>body {background-color: #ADD8E6;}</style>""", unsafe_allow_html=True)

    # Welcome message
    st.markdown("""
    ## Zambian Legislative Document Summarizer: Summarizer-knps

    Summarize long and complex Zambian legislative documents quickly and easily.

    *Benefits:*

    - Save time.
    - Understand key points better.
    - Identify key trends and patterns.
    - Make informed decisions.

    *Try it today!*
    """)

    # Instructions
    st.markdown("""
    *How to use:*

    1. Go to the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
    2. Copy the link to the PDF document.
    3. Paste the link into the Summarizer-KNPS interface and select the type of summary you want.
    4. Click the "Summarize" button.
    5. Read the summary!
    """)

    # User input for PDF link
    pdf_link = st.text_input("Paste the link to a PDF file:")

    if st.button("Summarize"):
        # Check if PDF link is empty
        if pdf_link:
            # Extract text from the PDF link
            pdf_text = extract_text_from_pdf_url(pdf_link)

            # Initialize tokenizer and model
            checkpoint = "google/pegasus-large"
            tokenizer = transformers.AutoTokenizer.from_pretrained(checkpoint)
            model = transformers.AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

            # Tokenize and summarize the content
            sentences = nltk.tokenize.sent_tokenize(pdf_text.strip())
            chunks = []

            for sentence in sentences:
                chunks.append(sentence)

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


if __name__ == "__main__":
    main()
