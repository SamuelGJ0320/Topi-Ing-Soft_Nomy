from django.core.management.base import BaseCommand
from restaurant.models import Restaurant
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Load restaurant from restaurants_descriptions.json into the Restaurant model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        #El path del archivo movie_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'restaurant_descriptions.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            restaurants = json.load(file)
        
        # Add products to the database
        cont = 0
        for restaurant in restaurants:
            restaurant_to_update = Restaurant.objects.filter(nombre = restaurant['nombre']).first()
            if not restaurant_to_update:
                print(f"{restaurant['nombre']} is not in the database")   
            else:           
                restaurant_to_update.descripcion = restaurant['description']
                restaurant_to_update.save()
                cont+=1
                    
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} descriptions to the database'))