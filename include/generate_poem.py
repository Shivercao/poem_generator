import os
import keras
import tempfile
from keras.models import load_model
import random
import numpy as np
from collections import Counter


"""
This class is used to generate poems,
it loads trained LSTM models and uses them to predict
the next character in a seed sentence recursively
until a poem is finished.
"""

class poemGenerator:
    def __init__(self, models_path, dp ):
        self.models_path = models_path
        self.dp = dp
        self.models = {}

    def load_trained_models(self):
        print("Loading models .. (I'm gonna use all of them)")
        for fname in os.listdir(self.models_path):
            key = fname[0:2]
            self.models[key] = load_model(os.path.join(self.models_path, fname))


    def get_char(self ,pred_list):
        frequencies = Counter(pred_list)
        freq_max = frequencies.most_common(2)
        top_char = freq_max[0][0]

        if len(freq_max) > 1:
            sec_char = freq_max[1][0]
        else:
            sec_char = freq_max[0][0]
        return top_char, sec_char


    def generate_poem(self, path ,num_poems=2 ,seed_length=50 , poem_length=200):

        print(r"I'm writing a poem, do not disturb")
        for poem_id in range(num_poems):

            poem = ''
            randint = random.randint(0, 1000000)
            starting_sentence = self.dp.corpus[randint:randint + seed_length]
            #starting_sentence = 'INSERT CUSTOM STARING SENTENCE HERE'
            poem += starting_sentence

            full_poem = '\033[1m' + poem + '\033[0m'

            for i in range(poem_length):

                indexes = []
                indexes2 = []
                for key ,model in self.models.items():

                    try:
                        key = int(key)
                        X_test = self.dp.onehot_characters(poem[-key+1:])

                        preds = model.predict(X_test, verbose=0)[0]
                        pred_char = np.argmax(preds)
                        preds[pred_char] *= 0.5
                        pred_char2 = np.argmax(preds)

                        index = pred_char
                        indexes.append(index)
                        indexes2.append(pred_char2)
                    except Exception as e:
                        print(e)
                        print('model ' + str(key) + ' trained with uncompatible number of characters')

                top_char, sec_char = self.get_char(indexes)
                top_char2, sec_char2 = self.get_char(indexes2)


                chosen = np.random.choice([top_char ,sec_char , top_char2, sec_char2] ,p=[0.6,0.1 , 0.3, 0.])
                new_letter = self.dp.characters[chosen]

                poem += new_letter
                full_poem += new_letter
                poem = poem[1:]

            full_poem_s = full_poem.split()
            full_poem_n = [word + '\n' if (count + 1) % 5 == 0 else word for count, word in enumerate(full_poem_s)]
            full_poem_n = ' '.join(full_poem_n)

            print(full_poem_n)

            fname = os.path.join(path, 'poem' + str(poem_id) + '.txt')
            with open(fname, 'w') as f:
                f.write(full_poem_n)
            print()



