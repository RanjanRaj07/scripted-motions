import spacy

class UseNLP:
    def getner(self, ipText):
        # nlp = spacy.load("en_core_web_sm")
        nlp_ner = spacy.load("./nlp-model/model-best")

        doc = nlp_ner(ipText)

        entities_dict = {}
        for ent in doc.ents:
            entities_dict[ent.text] = ent.label_

        # print('The default named entities are')
        # print(entities_dict)

        return entities_dict    
        