from dotenv import load_dotenv, find_dotenv
import json
import os
from openai import OpenAI
import numpy as np

_ = load_dotenv('api_keys_2.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openai_apikey'),
)

with open('restaurant_descriptions.json', 'r') as file:
    file_content = file.read()
    restaurants = json.loads(file_content)

#Esta función devuelve una representación numérica (embedding) de un texto, en este caso
#la descripción de las películas
    
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

emb = get_embedding(restaurants[1]['description'])
print(emb)

#Vamos a crear una nueva llave con el embedding de la descripción de cada película en el archivo .json


for i in range(len(restaurants)):
  emb = get_embedding(restaurants[i]['description'])
  restaurants[i]['embedding'] = emb


#Vamos a almacenar esta información en un nuevo archivo .json
file_name = 'restaurant_descriptions_embeddings.json'
with open(file_name, 'w') as file:
    json.dump(restaurants, file)