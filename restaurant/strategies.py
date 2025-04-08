import numpy as np
import openai
from .models import Restaurant

class EmbeddingStrategy:
    def process(self, prompt):
        raise NotImplementedError

class EmbeddingStrategy(EmbeddingStrategy):
    def get_embedding(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        response = openai.Embedding.create(input=[text], model=model)
        return response['data'][0]['embedding']

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def process(self, prompt):

        restaurants = Restaurant.objects.all()
        emb_request = self.get_embedding(prompt)
            
        sim = []
        for i in range(len(restaurants)):
            emb = restaurants[i].emb
            emb = list(np.frombuffer(emb))
            sim.append(self.cosine_similarity(emb, emb_request))
        sim = np.array(sim)
        idx = np.argmax(sim)
        idx = int(idx)

        if sim[idx] > 0:
            best_restaurant = [restaurants[idx]]
        else:
            best_restaurant = []
        return restaurants, best_restaurant