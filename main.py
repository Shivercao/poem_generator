from include.web_scrapper import *
from include.gen_corpus import *
from include.generate_poem import *
from include.manage_paths import *
from charlstm import *
import tempfile

"""
This is an example of an ensemble of character lstm networks
using a corpus of spanish poems with the purpose of generating
new ones.

the text  is obtained from 'http://amediavoz.com/'. The website
 is searched by the web_scrapper module to obtain all poems in it.
 
Text files with all poems of each author are saved to temp dir in an
intermediate step between web_scraping and charlstm.
These occupy aprox, 8Mb on disk so it shouldn´t be a problem.

Theres basically three clases
Data_Preparation to prepare data from corpus to input into the model
CharLSTM_Model which sets up LSTM model and trains it
PoemGenerator which generates poems using the trained models.

The whole process may take a while ..
 """

sentence_length_list = list(range(30,50,4)) # different models to train
all_paths = obtain_paths()

# Training of different 'sentence_length' LSTM models
for sentence_length in sentence_length_list:

    get_poems_from_website(all_paths['int_dir'])
    corpus = get_corpus_from_poems(all_paths['int_dir'])

    dp = Data_Preparation(corpus ,sentence_length=sentence_length)
    dp.setup_data(whole_words=False)


    model = CharLSTM_Model(dp.vectorized_data ,sentence_length=sentence_length)

    fname = all_paths['models_path']+ '\\' + str(sentence_length) + '.h5'
    model.setup_model()
    model.train_model(batch_size=200 ,epochs=10)
    model.save(fname)

# Poem generation
poem_generator = poemGenerator(all_paths['models_path'], dp)
poem_generator.load_trained_models()
poem_generator.generate_poem(path=all_paths['poems_dir'], num_poems=4)


