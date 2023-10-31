import streamlit as st
import transformers

# Name of the folder containing the pre-trained model
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the pre-trained model
model_checkpoint = "stjiris/t5-portuguese-legal-summarization"
t5_model = T5ForConditionalGeneration.from_pretrained(model_checkpoint)
t5_tokenizer = T5Tokenizer.from_pretrained(model_checkpoint)

# Preprocess the text to be summarized
preprocess_text = "These are some big words and text and words and text, again, that we want to summarize"
t5_prepared_text = "summarize: " + preprocess_text

# Encode the preprocessed text into tokens
tokenized_text = t5_tokenizer.encode(t5_prepared_text, return_tensors="pt").to("cuda")

# Generate a summary of the text
summary_ids = t5_model.generate(tokenized_text,
                                 num_beams=4,
                                 no_repeat_ngram_size=2,
                                 min_length=512,
                                 max_length=1024,
                                 early_stopping=True)

# Decode the summary IDs into text
output = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Print the summary to the console and to Streamlit
print("\n\nSummarized text: \n", output)
st.write("\n\nSummarized text: \n", output)
