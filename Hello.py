import streamlit as st

def run():
    """
    Runs the Summarizer-KNPS app.
    """

    # Page configuration
    st.set_page_config(
        page_title="Summarizer-KNPS",
        page_icon="📜"
    )

    # Set the background color to a light blue
    st.markdown(
        """
        <style>
        body {
            background-color: #ADD8E6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Instructions
    st.markdown(
        """
        **How to use Summarizer-KNPS:**

        1. Visit the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
        2. Copy the link to the PDF document.
        3. Select the type of summary.
        4. Paste the link into the Summarizer-KNPS interface and select the type of summary you want.
        5. Click the "Summarize" button.
        6. Read the summary!

        **Benefits of using Summarizer-KNPS:**

        - Save time by automatically summarizing long and complex legislative documents.
        - Better understand the key points of legislative documents.
        - Identify key trends and patterns in legislative documents.
        - Make informed decisions about Zambian legislation.

        *Try Summarizer-KNPS today and stay informed about Zambian legislation!*
        """
    )

if __name__ == "__main__":
    run()
    
