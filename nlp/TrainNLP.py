from spacy.tokens import DocBin
from tqdm import tqdm
import json
import spacy
import os

class TrainNLP:
    def train_nlp_model(self):
         #train new blank model
        nlp = spacy.blank("en") #load a new spacy model
        doc_bin = DocBin()
        count = 0

        f = open('./train-data/annot.json')
        train_data = json.load(f)

        #creating train.spacy from json file
        for text, annot in tqdm(train_data['annotations']):
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in annot["entities"]:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")

                if span is None:
                    print('skipping entity')
                    count+=1
                else:
                    ents.append(span)
                
                doc.ents = ents
                doc_bin.add(doc)

        print(f'Train data added to train.spacy with {count} entites skiped\n')
        doc_bin.to_disk("./nlp-model/train.spacy")

        try:
            #spaCy command to configure the blank nlp model
            command1 = 'py -m spacy init fill-config ./nlp-model/base_config.cfg ./nlp-model/config.cfg'
            exit_code1 = os.system(command1)
            if exit_code1==0:
                print('model configered\n')
            else:
                print(f'command failed with exit code: {exit_code1}')

            #spaCy command to train the blank nlp model with the data in train.spacy
            command2 = 'py -m spacy train ./nlp-model/config.cfg --output ./nlp-model --paths.train ./nlp-model/train.spacy --paths.dev ./nlp-model/train.spacy'
            exit_code2 = os.system(command2)
            if exit_code2==0:
                print('model trained\n')
            else:
                print(f'command failed with exit code: {exit_code2}')
            
        except Exception as e:
            print('An error occurred:', e)
        
        if exit_code1==0 and exit_code2==0:
            return 'model-trained'
        else:
            return 'error-in-model-training'


