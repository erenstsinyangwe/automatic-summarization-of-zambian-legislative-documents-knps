import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

# Load the Hugging Face models
checkpoint = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Streamlit app
st.title("Text Summarizer")

# User input for text
text_input = st.text_area("Enter the text:")

# Summarize the text
if st.button("Summarize"):
    with st.empty():
        st.text("Summarizing... Please wait.")

        # Tokenize the text
        tokenized_text = tokenizer.encode(text_input, return_tensors="pt")

        # Generate the summary
        output = model.generate(tokenized_text)

        # Decode the summary
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Display the summary
        st.header("Summarized Text:")
        st.write(generated_text)

        st.text("Summarization complete.")
