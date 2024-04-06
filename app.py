from sentence_transformers import SentenceTransformer
import numpy as np
from TTS.api import TTS
import faiss
import gradio as gr

from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine #importing real time tts

def read_text_from_file(file_path):
    with open(file_path, "r") as text_file:
        text = text_file.read()
    return text


text_file_path = "data.txt"
texts = read_text_from_file(text_file_path)
texts = texts.split("&&")

model = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')
# tts_model = TTS("tts_models/de/thorsten/tacotron2-DDC") #commenting for now

engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
stream = TextToAudioStream(engine)

doc_emb = model.encode(texts)
d = doc_emb.shape[1]  # Dimension of vectors
print(doc_emb.shape)
index = faiss.IndexFlatL2(d)
faiss.normalize_L2(doc_emb) #normalizing vectors
index.add(doc_emb)

def embed_query(query):
    query_emb = model.encode(query)
    return query_emb

def question(query):
  query_vector = np.asarray(embed_query(query))
  query_vector=np.expand_dims(query_vector,axis=0)
  faiss.normalize_L2(query_vector) #normalizing vectors
  print(query_vector.shape)
  k = 3 # Number of nearest neighbors to retrieve
  D, I = index.search(query_vector, k)
  relevant_paragraph=""
  for i in range(k):
    relevant_paragraph_index = I[0][i]
    relevant_paragraph += texts[relevant_paragraph_index] + "\n"


  # tts_model.tts_to_file(relevant_paragraph, file_path="./output.wav") generating audio only
  stream.feed(relevant_paragraph)
  stream.play()
  return relevant_paragraph

demo = gr.Interface(fn=question, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch()
    

