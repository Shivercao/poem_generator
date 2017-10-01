import os
from gensim.models import Word2Vec
import numpy as np
import pickle

subdir = r'E:\lstm_spanish\poem_sentences'
model = Word2Vec.load(r'E:\lstm_spanish\poem_model\model')

""" This script generates a pickle file from a list that contains
numpy arrays for each sentence (each word as vector) of all poems
of a single author"""

wordvec_dim = 100


for c , fname in enumerate(os.listdir(subdir)):

    full_name = os.path.join(subdir,fname)

    with open(full_name,'r') as f:
        text = f.read()

    text = text.split('\n')

    array_list = []

    for i ,sent in enumerate(text):
        sent_array = np.empty([len(sent.split()),wordvec_dim ])
        for j , word in enumerate(sent.split()):
            try:
                wordvec = np.reshape(model[word],[1,100])
                sent_array[j,:] = wordvec

            except:
                sent_array[j, :] = np.zeros([1, wordvec_dim])
        array_list.append(sent_array)


    if len(array_list) > 1:
        with open(r'E:\lstm_spanish\sentences_asarrays\author_' + str(c) + '.pkl','wb') as f:
            pickle.dump(array_list,f)



