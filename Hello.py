import streamlit as st

def run():
    """
    Summarize Zambian legislative documents using Summarizer-KNPS.
    """

    # Set page configuration
    st.set_page_config(
        page_title="Zambian Legislative Document Summarizer",
        page_icon="📜"
    )

    # Set background color
    st.markdown("""
        <style>body {background-color: #ADD8E6;}</style>
    """, unsafe_allow_html=True)

    # Welcome message
    st.markdown("""
        # Zambian Legislative Document Summarizer
        ## Summarizer-KNPS

        Quickly and easily summarize long and complex Zambian legislative documents.

        *Benefits:*

        - Save time.
        - Improve understanding of key points.
        - Discover key trends and patterns.
        - Make informed decisions.

        *Try it today!*
    """)

    # Instructions
    st.markdown("""
        *How to use:*

        1. Visit the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
        2. Copy the link to the PDF document.
        3. Choose the type of summary you want.
        4. Paste the link into the Summarizer-KNPS interface and select your desired summary type.
        5. Click the "Summarize" button.
        6. Read the summary!
    """)

if _name_ == "_main_":
    run()
