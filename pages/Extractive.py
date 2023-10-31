 st.write("Loaded")

# name of folder principal
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_checkpoint = "stjiris/t5-portuguese-legal-summarization"
t5_model = T5ForConditionalGeneration.from_pretrained(model_checkpoint)
t5_tokenizer = T5Tokenizer.from_pretrained(model_checkpoint)

preprocess_text = "These are some big words and text and words and text, again, that we want to summarize"
t5_prepared_Text = "summarize: "+preprocess_text
#print ("original text preprocessed: \n", preprocess_text)

tokenized_text = t5_tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


# summmarize 
summary_ids = t5_model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=512,
                                    max_length=1024,
                                    early_stopping=True)

output = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print ("\n\nSummarized text: \n",output)

st.write("\n\nSummarized text: \n",output)
