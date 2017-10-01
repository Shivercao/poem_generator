from __future__ import print_function
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM , Dense, Activation, Dropout
from keras.optimizers import RMSprop
import random
from keras import regularizers

"""
Two classes are defined here,

Data_Preparation class takes care of converting the corpus into
sentences of fixed length and then one hot encoding each character
of the sentence and stacking into an array. Each one of these arrays
is one training example, whilst the target is the upcoming character
in the sentence.

CharLSTM_Model sets up trains and saves a trained LSTM network
that goes over the training set epochs number of times
"""


class Data_Preparation:
    def __init__(self , corpus ,sentence_length=21):
        self.sentence_length = sentence_length
        self.corpus = corpus
        self.characters = sorted(list(set(self.corpus)))
        self.key_dict = {char : ind for ind , char in enumerate(self.characters)}
        self.vectorized_data = {}

        print('Total number of characters in corpus: ' + str(len(self.corpus)) + '\n')


    def setup_data(self , whole_words=False ):
        if whole_words:
            sentence_list = self.variable_sentence_maker()
        else:
            sentence_list = self.sentence_maker()
        data_array = self.sent2array(sentence_list)

        self.vectorized_data['y'] = data_array[:, -1, :]
        self.vectorized_data['X'] = data_array[:, 0:-1, :]



    # Returns array for one sentence
    def onehot_characters(self ,sentence):

        def char_assign(self ,char):
            arr = np.zeros([1, len(self.characters)])
            arr[0, self.key_dict[char]] += 1
            return arr

        vec_list = [char_assign(self ,char) for char in sentence]
        array = np.vstack(vec_list)
        return np.expand_dims(array , axis=0)

    # Returns a list with all sentences extracted from the text
    def sentence_maker(self ):
        print('Dividing corpus into sentennces ...\n')
        r = random.randint(0,8)
        sentence_list = [self.corpus[(i+r):(i+r)+self.sentence_length] for i in range(0, len(self.corpus)-1000, 10)]
        print(str(len(sentence_list)) + ' Sentences extracted  of length ' + str(self.sentence_length))
        random.shuffle(sentence_list)

        return sentence_list

    def variable_sentence_maker(self):
        print('Dividing corpus into sentences ...\n')
        words = self.corpus.split()
        sentences = []

        for word_len in range(4,20):
            aux = [' '.join(words[i:i+word_len]) for i in range(len(words)-8) if len(' '.join(words[i:i+word_len]))
                   == self.sentence_length and '.' not in ''.join(words[i:i+word_len])]
            sentences.extend(aux)

        random.shuffle(sentences)
        return sentences



    # Returns an array with all sentences represented as arrays (w one hot encoding of chars)
    def sent2array(self,sentence_list):
        print('Vectorizing sentences ...\n')
        array_list = [self.onehot_characters(sent) for sent in sentence_list]
        return np.vstack(array_list)



class CharLSTM_Model:
    def __init__(self , vectorized_data ,sentence_length=21):
        self.sentence_length = sentence_length
        self.X = vectorized_data['X']
        self.y = vectorized_data['y']
        self.n_characters = np.shape(self.y)[1]




    def setup_model(self):

        print('Setting up LSTM model')
        self.model = Sequential()
        self.model.add(LSTM(100, input_shape=(np.shape(self.X)[1], self.n_characters)))
        self.model.add(Dense(self.n_characters))
        self.model.add(Dropout(0.7))
        self.model.add(Activation('softmax'))

        optimizer = RMSprop(lr=0.001)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)


    # train the model, output generated text after each iteration
    def train_model(self, batch_size=200,epochs=10):
            self.model.fit(self.X, self.y,
                      batch_size=batch_size,
                      epochs=epochs)


    def save(self, fname):
        print('Saving '+fname +' model')
        self.model.save(fname)

