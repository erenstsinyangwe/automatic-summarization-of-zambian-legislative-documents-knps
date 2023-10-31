import streamlit as st
import subprocess
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Function to install requirements from requirements.txt
def install_requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.readlines()

    for requirement in requirements:
        subprocess.run(["pip", "install", requirement], capture_output=True)

# Function to summarize text using a pre-trained T5 model
def summarize_text():
    # Name of the folder containing the pre-trained model
    model_checkpoint = "stjiris/t5-portuguese-legal-summarization"
    t5_model = T5ForConditionalGeneration.from_pretrained(model_checkpoint)
    t5_tokenizer = T5Tokenizer.from_pretrained(model_checkpoint)

    # Preprocess the text to be summarized
    preprocess_text = "These are some big words and text that we want to summarize."
    t5_prepared_text = "summarize: " + preprocess_text

    # Encode the preprocessed text into tokens
    tokenized_text = t5_tokenizer.encode(t5_prepared_text, return_tensors="pt")

    # Generate a summary of the text
    summary_ids = t5_model.generate(
        tokenized_text,
        num_beams=4,
        no_repeat_ngram_size=2,
        min_length=512,
        max_length=1024,
        early_stopping=True
    )

    # Decode the summary IDs into text
    output = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output

# Main function to run the app
def main():
    # Install necessary requirements
    install_requirements()

    # Set page configuration
    st.set_page_config(
        page_title="Zambian Legislative Document Summarizer",
        page_icon="📜",
    )

    # Display the summarized text using Streamlit
    st.write("Summarized text:")
    summarized_text = summarize_text()
    st.write(summarized_text)

if _name_ == "_main_":
    main()
