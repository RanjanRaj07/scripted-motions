from TrainNLP import TrainNLP
from UseNLP import UseNLP
import os

model_path = './nlp-model/model-best'


def nlp_ner():
    ipText = input('enter the Text sentence\n')
    usenlp = UseNLP()
    entities_dict = usenlp.getner(ipText)
    print('The obtained named entities from the model are')
    print(entities_dict)

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
