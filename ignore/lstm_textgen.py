'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
#from import_corpora import text
import os
from gensim.models import Word2Vec
import pickle
from keras import backend as K



sequence_length = 5
batch_size = 100
wordvec_dim = 100
modelo = Word2Vec.load(r'E:\lstm_spanish\poem_model\model')

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.i = 0

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname),'rb') as f:
                sent_list = pickle.load(f)
                for sentences in sent_list:
                    yield sentences


sentences_iter = MySentences('E:\lstm_spanish\sentences_asarrays')

def batch_generator(sentences_iter , batch_size):

    #batch = np.empty([batch_size ,sequence_length , wordvec_dim])
    batch_list = []

    for sent in sentences_iter:
        sentence_length = np.shape(sent)[0]
        i = 0

        if sentence_length >= sequence_length:

            while i < (sentence_length - sequence_length):
                seq = sent[i: i + sequence_length, :]
                seq = np.reshape(seq, [1 ,sequence_length, wordvec_dim])
                batch_list.append(seq)
                i += 1

                if len(batch_list) == batch_size:
                    return np.vstack(batch_list)


# x  = batch_generator(sentences_iter, 200000)

with open('E:\lstm_spanish\X900k.npy','rb') as f:
    X = np.load(f)


# Extracting last word of each sequence as target value 'y'
y = X[:,-1,:]
X = X[: ,0:-1, :]


def cos_cost(y ,y_pred):

    dot = K.batch_dot(y, y_pred, axes=1)

    cosine_comp = K.abs(dot)

    print(y)
    norm_y = K.sqrt(K.sum(K.square(y), axis=1, keepdims=True))
    print(norm_y)
    norm_yp = K.sqrt(K.sum(K.square(y_pred), axis=1, keepdims=True))
    scale_comp = K.abs(norm_y-norm_yp)   # OPTION 1
    #scale_comp = K.square(y - y_pred)   # OPTION 2

    scale_comp *= scale_comp

    loss = cosine_comp + scale_comp

    return loss

def cos_distance(y_true, y_pred):

    print(y_true)
    print(y_pred)

    def l2_normalize(x, axis):
        norm = K.sqrt(K.sum(K.square(x), axis=axis, keepdims=True))
        return K.sign(x) * K.maximum(K.abs(x), K.epsilon()) / K.maximum(norm, K.epsilon())
    y_true = l2_normalize(y_true, axis=-1)
    y_pred = l2_normalize(y_pred, axis=-1)

    result = K.mean(y_true * y_pred, axis=-1)
    print(result)

    return result

"""dot = np.dot(y,y_pred)
    dot = dot / (np.linalg.norm(y) * np.linalg.norm(y_pred))
    dot_squared = dot * dot"""

print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(sequence_length-1, wordvec_dim)))
model.add(Dense(wordvec_dim))
model.add(Dropout(0.7))

optimizer = RMSprop(lr=0.0001,clipnorm=0.1)

model.compile(loss=cos_cost, optimizer=optimizer)

model.fit(X, y, batch_size=2000, epochs=10, verbose=1)




#print('Predicted words vs similar real words')
#print(modelo.wv.most_similar(y_pred , topn=4))
#print(modelo.wv.similar_by_vector(y[randint,:] , topn=4))

def poem_generator(poem_length):
    randint = np.random.randint(0, 100000)

    xss = X[randint, :, :]
    xs = np.reshape(xss, [1, 4, -1])

    starting_words = []

    for i in range(sequence_length-1):
        starting_words.append(modelo.wv.similar_by_vector(xss[i,:] , topn=4)[0][0])

    print(starting_words)
    poem = []
    poem.extend(starting_words)
    poemg = []
    poemg.extend(starting_words)

    for i in range(poem_length):

        y_pred = model.predict(xs, batch_size=1)

        xs [0 , 0:3 , :] = xs [0 , 1:4 , :]
        xs[0, 3, :] = y_pred
        y_pred = np.reshape(y_pred , [100])

        print(str(int(np.sum(np.square(y_pred)))) + ' prediction size')
        print(str(int(np.sum(np.square(y[randint + i,:])))) + ' real size')

        poemg.append(modelo.wv.similar_by_vector(y_pred , topn=4)[0][0])
        poem.append(modelo.wv.similar_by_vector(y[randint + i,:], topn=4)[0][0])

    return poem, poemg




poem, poemg = poem_generator(10)

print(poem)
print(poemg)

poem1, poemg1 = poem_generator(10)

print(poem1)
print(poemg1)

poem2, poemg2 = poem_generator(10)

print(poem2)
print(poemg2)


