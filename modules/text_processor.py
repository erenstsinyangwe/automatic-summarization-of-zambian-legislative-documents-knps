import re
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

def process_text(input_text):
    # Step 1: Lowercasing
    text = input_text.lower()

    # Step 2: Tokenization
    tokens = re.findall(r'\b\w+\b', text)

    # Step 3: Removing Punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    # Step 4: Stop Word Removal
    # from nltk.corpus import stopwords
    # stopwords = set(stopwords.words('english'))
    # tokens = [word for word in tokens if word not in stopwords]

    # Step 5: Stemming (Porter Stemmer)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    # Step 6: Removing Numbers
    stemmed_tokens = [word for word in stemmed_tokens if not word.isdigit()]

    # Step 7: Removing Extra Whitespace
    text = ' '.join(text.split())

    # Step 8: Encoding/Decoding
    text = text.encode('ascii', 'ignore').decode('utf-8')

    # Add a full stop after the first word
    first_space_index = text.find(' ')
    if first_space_index != -1:
        text = text[:first_space_index + 1] + '.' + text[first_space_index + 1:]

    return text
