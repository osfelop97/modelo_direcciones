import spacy

nlp = spacy.load("output/model-best")


# Texto de prueba
text = "false Cll 123 erg34thg3456h45 Clle edf"

# Procesar el texto
doc = nlp(text)

# Mostrar las entidades reconocidas
for ent in doc.ents:
    print(ent.text, ent.label_)