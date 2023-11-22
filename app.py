from flask import Flask, render_template, request
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import torch

app = Flask(__name__)

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text-summarization', methods=["POST"])
def summarize():
    if request.method == "POST":
        inputtext = request.form["inputtext_"]
        input_text = "summarize: " + inputtext
        tokenized_text = tokenizer.encode(input_text, return_tensors='pt', max_length=1024).to(device)
        summary_ = model.generate(tokenized_text, min_length=300, max_length=500)
        summary = tokenizer.decode(summary_[0], skip_special_tokens=True)
        return render_template("output.html", data={"summary": summary})

if __name__ == '__main__':
    app.run()