import streamlit as st
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

def calculate_word_count(text: str) -> int:
  """Calculates the word count of the given text.

  Args:
    text: A string containing the text to be counted.

  Returns:
    An integer representing the word count of the text.
  """

  words = text.split()
  return len(words)

def calculate_summary_percentage(word_count: int, summary_length: int) -> float:
  """Calculates the percentage of the content that is being summarized.

  Args:
    word_count: The word count of the entire text.
    summary_length: The length of the summary in words.

  Returns:
    A float representing the percentage of the content that is being summarized.
  """

  return summary_length / word_count * 100

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
          word_frequencies[word.lower()] += 1

  word_count = calculate_word_count(text)
  summary_length = int(word_count * (per / 100))

  # Select the top `per` percentage of sentences based on their word frequencies.
  sentence_scores = {}
  for sentence in sentences:
    for word in sentence.split():
      if word.lower() in word_frequencies:
        if sentence not in sentence_scores:
          sentence_scores[sentence] = word_frequencies[word.lower()]
        else:
          sentence_scores[sentence] += word_frequencies[word.lower()]

  select_length = summary_length
  summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
  summary = '. '.join(summary)

  # Return the summary with the word count and the percentage of the content that is being summarized.
  return f"Word count: {word_count}\nPercentage of content summarized: {per:.2f}%\n\nSummary:\n{summary}"

# Streamlit appimport streamlit as st
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

def calculate_word_count(text: str) -> int:
  """Calculates the word count of the given text.

  Args:
    text: A string containing the text to be counted.

  Returns:
    An integer representing the word count of the text.
  """

  words = text.split()
  return len(words)

def calculate_summary_percentage(word_count: int, summary_length: int) -> float:
  """Calculates the percentage of the content that is being summarized.

  Args:
    word_count: The word count of the entire text.
    summary_length: The length of the summary in words.

  Returns:
    A float representing the percentage of the content that is being summarized.
  """

  return summary_length / word_count * 100

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
          word_frequencies[word.lower()] += 1

  word_count = calculate_word_count(text)
  summary_length = int(word_count * (per / 100))

  # Select the top `per` percentage of sentences based on their word frequencies.
  sentence_scores = {}
  for sentence in sentences:
    for word in sentence.split():
      if word.lower() in word_frequencies:
        if sentence not in sentence_scores:
          sentence_scores[sentence] = word_frequencies[word.lower()]
        else:
          sentence_scores[sentence] += word_frequencies[word.lower()]

  select_length = summary_length
  summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
  summary = '. '.join(summary)

  # Return the summary with the word count and the percentage of the content that is being summarized.
  return f"Word count: {word_count}\nPercentage of content summarized: {per:.2f}%\n\nSummary:\n{summary}"

# Streamlit app