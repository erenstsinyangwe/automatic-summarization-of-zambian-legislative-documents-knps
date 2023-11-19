import streamlit as st

def authenticate_user():
    st.subheader("Authentication")

    # Ask for user name
    name = st.text_input("Enter your name:")

    # Ask for password
    password = st.text_input("Enter the password:", type="password")

    return name, password

def display_home_page():
    st.title("Welcome to the Zambian Automatic Summarization of Legislative Documents App")

    # Authenticate user
    name, password = authenticate_user()

    # Check if the entered password is correct
    if password == "knps":
        st.success(f"Welcome, {name}! You are authenticated.")

        st.markdown(
            """
            This app is designed to automatically extract, process, and summarize Zambian legislative documents.
            
            ## Instructions:
            1. Enter the PDF URL of a Zambian legislative document.
            2. Click the "Extract Text" button to initiate the text extraction process.
            3. The app will then process and summarize the extracted text.
            4. You can adjust the desired percentage for the summary length using the slider.
            
            ## Get Links to Documents:
            You can obtain links to Zambian legislative documents from the official [Parliament website](https://www.parliament.gov.zm/acts-of-parliament).
            """
        )

        # Automatically transition to the main app after successful authentication
        st.experimental_rerun()

    else:
        st.error("Authentication failed. Please enter the correct password to proceed.")
