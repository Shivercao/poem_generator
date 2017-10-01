import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import string
import unicodedata
import os

"""
Opens one author's poems at a time and processes them,
and writes the resulting sentences to a new line in a file
 
Basically text is lowercased, 'tildes' removed, and is tokenized in sentences.
"""

num = 1

for fname in os.listdir(r'C:\Users\mpozz\Documents\PycharmProjects\Otros\lstm\poem_by_author'):

    with open('poem_by_author/' + fname,'r') as f:
        text = f.read()

    # Set to remove punctuation
    punct_set = set(string.punctuation)
    punct_set.remove(',')
    punct_set.remove('.')
    punct_set.update('¿')

    # Remove punctuation except for commas and periods
    def remove_punct(text):
        return ''.join(ch for ch in text if ch not in punct_set)

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
    text = text.lower()

    sentences = nltk.sent_tokenize(text, language='spanish')


    # Writes a file with sentences in poems for each author
    subdir = 'E:\lstm_spanish\poem_sentences'
    file_name = 'sentences_' + str(num)
    with open(os.path.join(subdir, file_name),"w") as f:
        for s in sentences:
            s = s.replace('.', '')
            s = s.replace(',', '')
            s = ' '.join(s.split())
            if len(s.split()) > 3:
                f.write("%s\n" % s)

    num += 1
