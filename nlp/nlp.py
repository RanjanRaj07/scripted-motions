from TrainNLP import TrainNLP
from UseNLP import UseNLP
import os
from nltk.stem import PorterStemmer

# Initialize the Porter stemmer
porter = PorterStemmer()

model_path = './nlp-model/model-best'

# Function to perform stemming using NLTK's Porter stemmer
def stem_word(word):
    return porter.stem(word)


def nlp_ner():
    ipText = input('enter the Text sentence\n')
    usenlp = UseNLP()
    entities_dict = usenlp.getner(ipText)
    print('The obtained named entities from the model are')
    
    # Remove trailing and leading spaces from keys
    cleaned_dict = {key.strip(): value for key, value in entities_dict.items()}

    # Reverse keys and values
    reversed_dict = {value: key for key, value in cleaned_dict.items()}
    print(reversed_dict)
    
   # Perform stemming on the value associated with the 'ACTION' key
    action_stem = stem_word(reversed_dict['ACTION'])

    # Update the dictionary with the stemmed form of the verb
    reversed_dict['ACTION'] = action_stem
    
    print('After stemming')
    print(reversed_dict)


if os.path.exists(model_path):
    print('model exists\n')
    nlp_ner()
else:
    trainnlp = TrainNLP()
    code = trainnlp.train_nlp_model()
    if code == 'model-trained':
        print('model trained successfuly\n')
        nlp_ner()
    else:
        print(f'Error: {code}\n')

