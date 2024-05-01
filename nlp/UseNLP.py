import spacy

class UseNLP:
    def getner(self, ipText):
        #load the trained custome SpaCy nlp model
        nlp_ner = spacy.load("./nlp-model/model-best")

        doc = nlp_ner(ipText)

        entities_dict = {}
        for ent in doc.ents:
            entities_dict[ent.text] = ent.label_

        return entities_dict    
        