import csv
import spacy
from spacy.tokens import DocBin


# Crear el modelo en blanco para español

nlp = spacy.blank("es")

# Leer el archivo CSV con las entidades y generar patrones
patterns = []
with open("entidades.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        label = row["Significado"]
        palabras = [p.strip() for p in row["Palabra"].split(",") if p.strip()]
        for palabra in palabras:
            patterns.append({"label": label, "pattern": palabra})

# Agregar el componente EntityRuler y cargar los patrones
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)

# Leer el corpus desde el CSV
corpus = []
with open("rues(in).csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        corpus.append(row["Data"])


# Obtener todas las etiquetas únicas para encabezados CSV
labels = sorted(set(pattern['label'] for pattern in patterns))

# Crear archivo CSV resultante con anotaciones
with open("resultado_entidades.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Escribir encabezado
    writer.writerow(["Texto"] + labels)

    for text in corpus:
        doc = nlp(text)
        # Crear diccionario vacío para almacenar entidades por etiqueta
        entidades_dict = {label: set() for label in labels}

        # Llenar diccionario con entidades detectadas (sin repetidos)
        for ent in doc.ents:
            entidades_dict[ent.label_].add(ent.text)

        # Preparar la fila para escribir en CSV
        fila = [text] + [", ".join(sorted(entidades_dict[label])) for label in labels]

        # Escribir la fila en CSV
        writer.writerow(fila)

# # Crear el corpus anotado (para visualizar y depurar)
# annotated_corpus = []
# for text in corpus:
#     doc = nlp(text)
#     entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
#     annotated_corpus.append((text, {"entities": entities}))
#
# print(annotated_corpus)
#
# # Mostrar las anotaciones generadas
# for text, annotations in annotated_corpus:
#     print("Texto:", text)
#     print("Anotaciones:", annotations)
#     print("------")
#
# # Dividir los datos en dos partes: entrenamiento y desarrollo (dev)
# split_index = len(annotated_corpus) // 2
# train_data = annotated_corpus[:split_index]
# dev_data = annotated_corpus[split_index:]
#
# # Crear objetos DocBin para entrenamiento y dev
# doc_bin_train = DocBin()
# doc_bin_dev = DocBin()
#
# def add_docs_to_docbin(data, doc_bin):
#     for text, annotations in data:
#         doc = nlp(text)
#         spans = []
#         for start, end, label in annotations["entities"]:
#             span = doc.char_span(start, end, label=label)
#             if span is None:
#                 print(f"Advertencia: No se pudo crear el span para '{text}' con los índices {start}-{end}")
#                 continue
#             spans.append(span)
#         doc.ents = spans
#         doc_bin.add(doc)
#
# # Procesar y agregar los datos a cada DocBin
# add_docs_to_docbin(train_data, doc_bin_train)
# add_docs_to_docbin(dev_data, doc_bin_dev)
#
# # Guardar los archivos binarios
# doc_bin_train.to_disk("train.spacy")
# doc_bin_dev.to_disk("dev.spacy")
