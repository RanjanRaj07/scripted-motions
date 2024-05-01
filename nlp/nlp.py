#from TrainNLP import TrainNLP
#from UseNLP import UseNLP
import TrainNLP
import UseNLP
import os
import sys

model_path = './nlp-model/model-best'


def nlp_ner():
    ipText = sys.argv
    ipText.pop(0)
    text = ''
    for word in ipText:
        text += word
        text += ' '
    usenlp = UseNLP()
    text = text.split(".")
    output = []
    for line in text :
        output.append(usenlp.getner(line))
    # entities_dict = usenlp.getner(ipText)
    print('The obtained named entities from the model are')
<<<<<<< HEAD
    print(output)
=======
    
    # Remove trailing and leading spaces from keys
    cleaned_dict = {key.strip(): value for key, value in entities_dict.items()}

    # Reverse keys and values
    reversed_dict = {value: key for key, value in cleaned_dict.items()}
    print(reversed_dict)
>>>>>>> e5e01e0dd244a9fd337345b49cf5dbe48849ecc5

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

