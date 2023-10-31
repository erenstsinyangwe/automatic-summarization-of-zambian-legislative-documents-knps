import streamlit as st
import logging

def main():
    """
    Runs the Summarizer-KNPS app.
    """

    # Logger
    logger = logging.getLogger(_name_)
    logger.setLevel(logging.INFO)

    # Page configuration
    st.set_page_config(
        page_title="Summarizer-KNPS",
        page_icon="📜"
    )

    # Topbar
    st.title("Summarizer-KNPS: Your Gateway to Effortless Zambian Legislative Document Summarization")

    # Type of summary selection
    summarization_type = st.selectbox(
        "Select the type of summary:",
        ["Abstractive", "Extractive"]
    )

    # Instructions
    st.markdown(
        """
        *How to use Summarizer-KNPS:*

        1. Visit the [National Assembly Parliament website](https://www.parliament.gov.zm/acts-of-parliament) and find the PDF document you want to summarize.
        2. Copy the link to the PDF document.
        3. Select the type of summary.
        4. Paste the link into the Summarizer-KNPS interface and select the type of summary you want.
        5. Click the "Summarize" button.
        6. Read the summary!

        *Benefits of using Summarizer-KNPS:*

        - Save time by automatically summarizing long and complex legislative documents.
        - Better understand the key points of legislative documents.
        - Identify key trends and patterns in legislative documents.
        - Make informed decisions about Zambian legislation.

        *Try Summarizer-KNPS today and stay informed about Zambian legislation!*
        """
    )

    # Navigation based on user's selection
    if summarization_type == "Abstractive":
        st.markdown("You can navigate to the Abstractive page [here](pages/Abstractive.py).")
        logger.info("User selected Abstractive summarization")
    elif summarization_type == "Extractive":
        st.markdown("You can navigate to the Extractive page [here](pages/Extractive.py).")
        logger.info("User selected Extractive summarization")
    else:
        st.error("Invalid summarization type selected")
        logger.error("Invalid summarization type selected")

if _name_ == "_main_":
    main()
