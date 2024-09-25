from django.core.management.base import BaseCommand
from restaurant.models import Restaurant
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        ##Código para leer los embeddings del archivo movie_descriptions_embeddings.json
        json_file_path = 'restaurant_descriptions_embeddings.json'
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            restaurants = json.load(file)       
  
        for restaurant in restaurants:
            emb = restaurant['embedding']
            emb_binary = np.array(emb).tobytes()
            item = Restaurant.objects.filter(nombre = restaurant['nombre']).first()
            item.emb = emb_binary
            item.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated item embeddings'))        
        