import os
import openai
import numpy as np
import json
from dotenv import load_dotenv
from .models import Restaurant

load_dotenv('api_keys_1.env')
load_dotenv('api_keys_2.env')

openai.api_key = os.getenv('openai_apikey')

class EmbeddingRecommender:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'restaurant_descriptions.json'), 'r', encoding='utf-8') as f:
            self.restaurant_data = json.load(f)

        with open(os.path.join(base_dir, 'restaurant_descriptions_embeddings.json'), 'r', encoding='utf-8') as f:
            self.embeddings_data = json.load(f)

    def get_embedding(self, text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']

    def cosine_similarity(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def get_recommendations(self, prompt, top_n=3):
        user_embedding = self.get_embedding(prompt)

        similarities = []
        for idx, embedding in enumerate(self.embeddings_data):
            sim = self.cosine_similarity(user_embedding, embedding)
            similarities.append((idx, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)

        top_indices = [idx for idx, _ in similarities[:top_n]]

        all_restaurants = Restaurant.objects.all()
        recommended_restaurants = []

        for idx in top_indices:
            name = self.restaurant_data[idx]['name']
            matching = all_restaurants.filter(nombre=name).first()
            if matching:
                recommended_restaurants.append(matching)

        return all_restaurants, recommended_restaurants
