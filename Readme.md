Disclaimer (There's still a lot of room for improvement, also ignore the ignore folder its working progress)

## Synopsis

This is an example of a Recurrent neural network (LSTM) implementation in Keras with Tensorflow backend. 

The objective is get the computer to write poems (in Spanish). In order to do so the network is trained to predict the next character in a given sentence, hence, when provided a seed sentence to create a poem the network can predict the next character to extend it and repeat it many times until the poem is finished.

## Data

Training data consists of a collection of poems in spanish which are scrapped from the website http://amediavoz.com/. The corpus length in characters is about 6.7 Million.

Each training sample consist of a sentence in wich each character is one hot encoded to a vector, and the sequence of characters is stacked in an array.

## Model

### LSTM Network
- LSTM cell
  - Number of units = 100
  - Activation => tanh
  - Recurrent Activation => Hard sigmoid
- Dense Layer
  - Dropout = 0.7
- Softmax layer


## Usage

Run the main.py file, the data will be obtained by the web_scrapper module from the web and training begin, files are saved in tempdir. 

## From the model to a poem.

So in order to generate a poem once the model is trained a sentence is fed to the model and it predicts the next character recursively until the poem is finished. One problem encountered in with this approach is that often the model overfitted the data causing to repeat the same sentence over and over. LSTM networks are tricky to regularize so I opted for instead training different models and using the ensemble of these to generate the poem. So which models ? A model was trained for different sentences lengths as inputs, simply the corpus was chopped into different lengths and a model trained for each sentence length. So now instead of having one model predict the next character the ensemble of models is used, thus reducing the amount of undesired memorizing and overfitting.

### Packages used

**Library** | **Version**
--- | ---
**BeautifulSoup** | **4.6.0**
**Keras** | **2.0.8**
**Numpy** | **1.13.0** 
**Tensorflow** | **1.3.0** 
**Tensorflow_gpu** | **1.3.0** 
**Pickle** |  *  

### Python 3.5.4 was used

## Tests

So here are some of the generated poems:
(Theres still a lot to work on. Also, newlines are introduced by hand the model just outputs a string)

Aclarations:
- Seed sentence fed to the model is bold.
- Newlines and uppercasing of the first letter is done by hand
- I've also trimmed the end of the poem so it doesn't end in the middle of a word

### Poem 1
 *__Ayer naciste, y moriras mañana.	<br />		 
 para tan breve ser__ <br />		 
 esperando el alto de tu corazon <br />		 
 esta epoca es lo que <br />		 
 el mundo de tiempos de <br />			 
 los pensamientos de los pared,	<br />			 
 en el amor	<br />			 
 en el amor	<br />				 
 de los cabezos si	<br />
 el alma de tu corazon <br />
 de la mas alto esta <br />
 el cielo.* <br />

 ### Poem 2
 
 *__Atare mi caballo del tronco__ <br />
 __de algun arbol__, <br />
 el corazon de las peras <br />
 de tus pechos y los pechos <br />
 de los corazos, <br />
 en la marca <br />
 en el amor <br />
 es el corazon <br />
 en el canto <br />
 es mano de los pesames <br />
 es el consentio de ti <br />
 alma de ti me amor, <br />
 el amor es <br />
 es espejado de tus peros.* <br />


## Conclusion

Almost every word the model generates character wise makes sense, so thats good news. However the phrases generated only occasionally make sense. I'm currently working on how to input LDA topic modeling into the poem generation process in order to make it more meaningfull. However, getting a computer to write meaningful poems is a very complex task which I believe would require a lot more time and effort than I invested in this proyect, since my goal was rather academic/discovering oriented. 

Checkout - [This](https://en.wikipedia.org/wiki/Colorless_green_ideas_sleep_furiously) wiki article about the difference in semantic and grammatic coherence.

## Contact

Any kind of comments, corrections, contributions are welcome, contact me at mapozzi@gmail.com