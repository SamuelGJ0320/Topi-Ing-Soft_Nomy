from django.core.management.base import BaseCommand
from restaurant.models import Restaurant
import os
import json

class Command(BaseCommand):
    help = 'Load restaurants from json file to database'

    def handle(self, *args, **kwargs):
        json_file_path = 'restaurant/management/commands/restaurants.json'

        # Load data from json file
        with open(json_file_path, 'r') as file:
            restaurants = json.load(file)

        # Add data to database
        for i in range(50):
            restaurant = restaurants[i]
            exist = Restaurant.objects.filter(nombre=restaurant['nombre']).first()
            if not exist:
                Restaurant.objects.create(
                    nombre=restaurant['nombre'],
                    latitud=restaurant['latitud'],
                    longitud=restaurant['longitud'],
                    image='media/nomy/images/default.jpeg'
                )