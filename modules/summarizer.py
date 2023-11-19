from transformers import pipeline, BartTokenizer, BartForConditionalGeneration

def abstractive_summarize(text, summary_percentage=20):
    # Load pre-trained BART model and tokenizer
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

    # Calculate the desired summary length based on the percentage of the original text
    max_length = int(len(inputs["input_ids"][0]) * (summary_percentage / 100))

    # Generate the summary
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, length_penalty=3.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
