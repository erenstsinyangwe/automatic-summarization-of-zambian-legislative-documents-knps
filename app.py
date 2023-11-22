from flask import Flask, render_template, request
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import torch
from pdfminer.high_level import extract_text

app = Flask(__name__)

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)

@app.route('/')
def home():
    return render_template('index.html')

def summarize_text(input_text):
    input_text = "summarize: " + input_text
    tokenized_text = tokenizer.encode(input_text, return_tensors='pt', max_length=1024).to(device)
    summary_ = model.generate(tokenized_text, min_length=300, max_length=500)
    summary = tokenizer.decode(summary_[0], skip_special_tokens=True)
    return summary

@app.route('/text-summarization', methods=["POST"])
def summarize():
    if request.method == "POST":
        pdf_link = request.form.get("pdf_link")

        if pdf_link:
            try:
                # Extract text from the PDF link using pdfminer.six
                text = extract_text(pdf_link)

                # Perform summarization
                summary = summarize_text(text)

                return render_template("output.html", summary=summary)
            except Exception as e:
                error_message = f"Error processing PDF: {str(e)}"
                return render_template('index.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
