import streamlit as st

def run():
  """
  Runs the Summarizer-KNPS app.
  """

  # Page configuration
  st.set_page_config(
    page_title="Automatic Zambian Legislative Documents Summarizer",
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

  # Welcome message
  st.markdown(
    f"""
    ## Welcome to Summarizer-KNPS, the automatic Zambian legislative documents summarizer!

    With Summarizer-KNPS, you can quickly and easily summarize long and complex legislative documents, saving you time and effort. Simply paste in the link to the PDF document you want to summarize and select the type of summary you want. Summarizer-KNPS will then generate a summary of the document, highlighting the key points and trends.

    **Benefits of using Summarizer-KNPS:**

    * Save time by automatically summarizing long and complex legislative documents.
    * Better understand the key points of legislative documents.
    * Identify key trends and patterns in legislative documents.
    * Make informed decisions about Zambian legislation.

    **Try Summarizer-KNPS today and stay informed about Zambian legislation!**
    """
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
    """
  )

if __name__ == "__main__":
  run()
