from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
import json
import spacy
import os

class TrainNLP:
    def train_nlp_model(self):
        with open('./train-data/Corona2.json','r') as f:
            data = json.load(f)

        training_data = []

        for example in data['examples']:
            temp_dict = {}
            temp_dict['text'] = example['content']
            temp_dict['entities'] = []
            for annotation in example['annotations']:
                start = annotation['start']
                end = annotation['end']
                label = annotation['tag_name'].upper()
                temp_dict['entities'].append((start,end,label))
            training_data.append(temp_dict)
        # print(training_data[0])

        #train new blank model
        nlp = spacy.blank("en") #load a new spacy model
        doc_bin = DocBin()

        for training_example in tqdm(training_data):
            text = training_example['text']
            labels = training_example['entities']
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in labels:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                count = 0
                if span is None:
                    count += 1
                else:
                    ents.append(span)
        
            filtered_ents = filter_spans(ents)
            doc.ents = filtered_ents
            doc_bin.add(doc)
        print(f'Train data added to train.spacy with {count} entites skiped\n')
        doc_bin.to_disk("./nlp-model/train.spacy")

        try:
            command1 = 'py -m spacy init fill-config ./nlp-model/base_config.cfg ./nlp-model/config.cfg'
            exit_code1 = os.system(command1)
            if exit_code1==0:
                print('model configered\n')
            else:
                print(f'command failed with exit code: {exit_code1}')

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

# Racecadotril an antisecretory medication may be used to treat diarrhea 

