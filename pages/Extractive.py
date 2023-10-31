import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Name of the folder containing the pre-trained model
model_checkpoint = "stjiris/t5-portuguese-legal-summarization"

# Function to summarize text using the pre-trained T5 model
def summarize_text(text):
    # Load the pre-trained model
    t5_tokenizer = T5Tokenizer.from_pretrained(model_checkpoint)
    t5_model = T5ForConditionalGeneration.from_pretrained(model_checkpoint)

    # Preprocess the text to be summarized
    t5_prepared_text = "summarize: " + text

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
    # Set page configuration
    st.set_page_config(
        page_title="Zambian Legislative Document Summarizer",
        page_icon="📜",
    )

    # Get the text to be summarized from the user
    input_text = st.text_area("Text to summarize:")

    # Summarize the text
    summarized_text = summarize_text(input_text)

    # Display the summarized text
    st.write("Summarized text:")
    st.write(summarized_text)

#if __name__ == "__main__":
    #main()
