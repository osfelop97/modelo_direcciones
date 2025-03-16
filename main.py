import spacy
import cupy

# Esta función lanza un error si no hay GPU disponible
#spacy.require_gpu()
print(cupy.__version__)