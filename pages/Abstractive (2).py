import heapq
from typing import Dict, List, Union

def extract_pdf_text(pdf_link: str) -> str:
  """Extracts text from a PDF file at the given link.

  Args:
    pdf_link: A string containing the link to the PDF file.

  Returns:
    A string containing the extracted text from the PDF file.
  """

  try:
    response = requests.get(pdf_link)
    with open("temp.pdf", "wb") as pdf_file:
      pdf_file.write(response.content)
    text = extract_text("temp.pdf")
  except Exception as e:
    raise RuntimeError(f"Failed to extract text from PDF file: {e}")
  return text

def format_text(content: str) -> str:
  """Formats the given text by replacing multiple whitespaces with a single space and replacing newline characters with a line break.

  Args:
    content: A string containing the text to be formatted.

  Returns:
    A string containing the formatted text.
  """

  content = re.sub(r"\s+", " ", content)
  content = re.sub(r"\n", "\n", content)
  return content

def summarize(text: str, per: float) -> str:
  """Summarizes the given text by selecting the top `per` percentage of sentences based on their word frequencies.

  Args:
    text: A string containing the text to be summarized.
    per: A float between 0 and 100 representing the percentage of sentences to be selected for the summary.

  Returns:
    A string containing the summary of the text.
  """

  sentences = text.split(". ")
  word_frequencies = {}
  for sentence in sentences:
    for word in sentence.split():
      if word.lower() not in punctuation:
        if word.lower() not in word_frequencies:
          word_frequencies[word.lower()] = 1
        else:
          word_frequencies[word.lower()] +=
