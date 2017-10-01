from nltk.stem.wordnet import WordNetLemmatizer
import string
import unicodedata
import os
import re
import sys
"""
Opens one author's poems at a time and processes them,
and writes the resulting sentences to a new line in a file

Basically text is lowercased, 'tildes' removed, and is tokenized in sentences.
"""

def get_corpus_from_poems(files_dir):
    num = 1
    corpus = ''

    for fname in os.listdir(files_dir):

        with open(os.path.join(files_dir,fname), 'r') as f:
            text = f.read()

        # Set to remove punctuation
        punct_set = set(string.punctuation)
        punct_set.remove(',') # Do not remove, useful for sent tokenizing
        punct_set.remove('.') # Do not remove, useful for sent tokenizing
        punct_set.update('¿') # Added since not in string.punctuation



        # Remove punctuation except for commas and periods
        def remove_punct(text):
            return ''.join(ch for ch in text if ch not in punct_set)

        def remove_special_chars(text):
            text = re.sub('[¢£¤§©ª«®°²³·¹º»´–—’“”…‹]', "", text)
            text = re.sub('\.', ". ", text)
            text = re.sub('[0123456789]', ' ', text)
            text = re.sub('\xad', ' ', text)
            text = re.sub(' +', ' ', text)
            return text

        # Lemmatize words in text. (not used currently)
        lemmatizer = WordNetLemmatizer()
        def lemmatize(text):
            lem_text = " ".join(lemmatizer.lemmatize(word) for word in text.split())
            return lem_text

        # Eliminates 'tildes'
        def elimina_tildes(text):
            return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

        text = elimina_tildes(text)
        text = remove_punct(text)
        text = remove_special_chars(text)
        text = text.lower()

        corpus += text
        num += 1


    print('Corpus is: ' + str(sys.getsizeof(corpus) / 1000000) + ' Mbs')

    return corpus
