import os
from gensim.models import Word2Vec
import re

""" 
In this script the Word2Vec model is generated

There is a Helper class to feed sentences to the model
training as they are read.  This is memory friendly since
once used sentences are discarded."""



class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('E:\lstm_spanish\poem_sentences')

print('generating model ...')
print('skipped')
#model = Word2Vec(sentences, size=100)

print('saving restoring model')
#model.save(r'E:\lstm_spanish\poem_model\model')
model = Word2Vec.load(r'E:\lstm_spanish\poem_model\model')


with open('E:\lstm_spanish\poem_sentences\sentences_1','r') as f:
    sample_sentences = f.read()

sample_sentences = re.sub('\n', ' ', sample_sentences)

word_list = sample_sentences.split()

print(type(sample_sentences))

in_vocab_count = 0
not_in_vocab_count = 0
for word in word_list:
    if word in model.wv.vocab:
        in_vocab_count += 1
        #print(word + ' is in vocab')
    else:
        not_in_vocab_count += 1
        #print(word + ' is NOT in vocab')

total = in_vocab_count + not_in_vocab_count
print(str(in_vocab_count/total*100) + ' % of words are in model')